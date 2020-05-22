"""
Baseline class for `Good Reads` objects.
This class handles connection to `Good Reads` server.
"""

import string
from abc import ABC, abstractmethod

from .connect import connect
from .utils import *
from scrapereads import scrape


class GoodReadsMeta(ABC):
    """Defines the base of all `Good Reads` objects, that scrape and extract online data.

    * :attr:`base`: base page of the `Good Reads`.

    * :attr:`href`: href of a page.

    * :attr:`url`: url page of a `Good Reads` element.

    """

    def __init__(self):
        self.base = f'https://www.goodreads.com'
        self.href = '/'
        self._soup = None

    @property
    def url(self):
        if self.href:
            return self.base + self.href
        return None

    @url.setter
    def url(self, value):
        raise AttributeError('Cannot modify an URL directly. Please modify it through `base` and `href` attributes.')

    def _next_page(self, npage=1):
        page = f'?page={npage}' if npage > 1 else ''
        return page

    def connect(self, href=None):
        """Connect to a `Good Reads` page.

        Args:
            href (string, optional): if provided, connect to the page reference, else connect to the main page.

        Returns:
            bs4.element.Tag

        """
        url = self.base + (href or self.href)
        return connect(url)


class AuthorMeta(GoodReadsMeta):
    """Defines an abstract author, from the page info from ``https://www.goodreads.com/``.

    * :attr:`author_name`: name of the author.

    * :attr:`author_id`: key id of the author.

    * :attr:`base`: base page of `Good Reads`.

    * :attr:`href`: href page of the author.

    * :attr:`url`: url page of the author.

    """

    def __init__(self, author_id, author_name=None):
        super().__init__()
        # Connect to the author page to find out its name
        href = f'/author/show/{author_id}'
        if not author_name:
            self._soup = self.connect(href=href)
            author_name = scrape.get_author_name(self._soup)
        # Save attribute
        self.author_id = author_id
        self.author_name = author_name.replace('_', ' ').title()
        self.href = f'/author/show/{author_id}.{name_to_goodreads(self.author_name)}'

    # TODO: finish and add nested JSON option
    @abstractmethod
    def to_json(self):
        """Encode the author to a JSON format.

        Returns:
            dict

        """
        data = {
            'author': self.author_name,
            **self.get_info()
        }
        return data

    def __repr__(self):
        rep = f'Author: {self.author_name}'
        return rep


class BookMeta(AuthorMeta):
    """Abstract Book class, used as baseline.

    * :attr:`author_name`: name of the author.

    * :attr:`author_id`: key id of the author.

    * :attr:`book_name`: name of the book.

    * :attr:`book_id`: key if of the book.

    * :attr:`year`: year of publication of the book.

    * :attr:`edition`: edition of the book.

    * :attr:`base`: base page of `Good Reads`.

    * :attr:`href`: href page of the book.

    * :attr:`url`: url page of the book.

    """

    def __init__(self, author_id, book_id, book_name=None, author_name=None, edition=None, year=None):
        super().__init__(author_id, author_name=author_name)
        self.book_id = book_id or 0
        self.book_name = string.capwords(book_name, sep=None) if book_name else 'Unknown'
        self.edition = edition
        self.year = year
        self.href = f'/book/show/{self.book_id}.{name_to_goodreads(self.book_name)}'
        self._author = None

    def get_author(self):
        """Get the author pointing to the quote.

        Returns:
            Author

        """
        return self._author

    def register_author(self, author):
        """Point a quote to an Author.

        Args:
            author (Author): author to link the quote.

        """
        self._author = author

    @abstractmethod
    def to_json(self, encode='ascii'):
        """Encode the book to a JSON format.

        Returns:
            dict

        """

        # Default data, without any encoding
        raise NotImplementedError

    def __repr__(self):
        rep_ed = f', {self.edition}' if self.edition else ''
        rep_year = f' ({self.year})' if self.year else ''
        rep = f'{self.author_name}: "{self.book_name}"{rep_ed}{rep_year}'
        return rep


class QuoteMeta(AuthorMeta):
    """Defines a quote from the quote page from ``https://www.goodreads.com/author/quotes/``.

    * :attr:`quote_id`: nif of the quote.

    * :attr:`book_name`: name of the book / title.

    * :attr:`book_name`: name of the book / title.

    * :attr:`book_name`: name of the book / title.

    * :attr:`quote`: text.

    """

    def __init__(self, author_id, quote_id, quote_name=None, text=None, author_name=None, tags=None, likes=None):
        super().__init__(author_id, author_name=author_name)
        self.quote_id = quote_id
        self.quote_name = quote_name
        self.text = text or ''
        self.tags = tags or []
        self.likes = likes
        self._book = None
        self._author = None

    def get_author(self):
        """Get the author pointing to the quote.

        Returns:
            Author

        """
        return self._author

    def get_book(self):
        """Get the book pointing to the quote.

        Returns:
            Book

        """
        return self._book

    def register_author(self, author):
        """Point a quote to an Author.

        Args:
            author (Author): author to link the quote.

        """
        self._author = author

    def register_book(self, book):
        """Point a quote to a Book.

        Args:
            book (Book): book to link the quote.

        """
        self._book = book

    @abstractmethod
    def to_json(self, encode='ascii'):
        """Encode the quote to a JSON format.

        Returns:
            dict

        """
        raise NotImplementedError

    def __repr__(self):

        # Template:
        #   “quote here”
        #    ― Author Name, from "Book Name" (year)
        #      Likes: n, Tags, some, tags, here

        book = self.get_book()
        rep_book = f', from "{book.book_name}"' if book and book.book_name else ''
        rep_year = f' ({book.year})' if book and book.year else ''
        rep_tags = f", Tags: {', '.join(self.tags)}" if len(self.tags) > 0 else ''
        rep_likes = f'Likes: {self.likes}'
        rep_info = f'\n  {rep_likes}{rep_tags}'
        rep = f'“{self.text}”\n― {self.author_name}{rep_book}{rep_year}{rep_info}'
        return rep
