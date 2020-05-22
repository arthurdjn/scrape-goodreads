"""
Defines an Author from ``Good Reads``.
Connect to https://www.goodreads.com/ to extract quotes and books from famous authors.
"""

import warnings
import langdetect

from scrapereads.utils import *
from scrapereads import scrape
from scrapereads.meta import AuthorMeta
import scrapereads.reads as greads


class Author(AuthorMeta):
    """
    Defines an author, from the page info from ``https://www.goodreads.com/``.

    * :attr:`name`: name of the author.

    * :attr:`key`: key id of the author.

    * :attr:`url`: url page of the author.

    """

    def __init__(self, author_id, author_name=None):
        super().__init__(author_id, author_name=author_name)
        self._quotes = []
        self._books = []
        self._info = None

    @classmethod
    def from_url(cls, url):
        """Construct the class from an url.

        Args:
            url (string): url.

        Returns:
            Author

        """
        author_id = eval(url.split('/')[-1].split('.')[0])
        author_name = url.split('/')[-1].split('.')[1]
        return Author(author_id, author_name=author_name)

    def get_info(self):
        """Get author information (genres, influences, description etc.)

        Returns:
            dict

        """
        if not self._info:
            soup = self._soup or self.connect()
            self._info = scrape.get_author_info(soup)
        return self._info

    def add_quote(self, quote):
        """Add a quote to an Author.

        Args:
            quote (Quote or string): quote or text to add.

        """
        quote.author_name = self.author_name
        quote.author_id = self.author_id
        quote.register_author(self)
        self._quotes.append(quote)

    def add_book(self, book):
        """Add a book to an Author.

        Args:
            book (Book): book or book's name to add.

        """
        book.author_name = self.author_name
        book.author_id = self.author_id
        book.register_author(self)
        self._books.append(book)

    def _search_books(self):
        # Scrape books from tha author book page from scrapereads.com
        self._books = []
        npage = 1
        href = f'/author/list/{self.author_id}.{name_to_goodreads(self.author_name)}'
        search = True

        while search:
            # Didn't found any quotes
            search = False
            # Navigate through the next page
            href_page = href + self._next_page(npage=npage)
            soup = self.connect(href=href_page)
            npage += 1
            for book_tr in scrape.scrape_author_books(soup):
                # Books found
                search = True
                book_title = scrape.get_author_book_title(book_tr)
                book_href = book_title.get('href')
                book_id = book_href.split('/')[-1].split('-')[0].split('.')[0]
                book_name = book_title.text.strip().title()
                ratings = scrape.get_author_book_ratings(book_tr).contents[-1]
                edition = scrape.get_author_book_edition(book_tr)
                edition = edition.text.strip() if edition else None
                year = scrape.get_author_book_date(book_tr)
                book = greads.Book(self.author_id, book_id, book_name=book_name,
                                   author_name=self.author_name, edition=edition, year=year, ratings=ratings)
                self.add_book(book)
                yield book

    def _search_quotes(self):
        # Scrape quotes from the author qutoe page from scrapereads.com
        self._quotes = []
        npage = 1
        href = f'/author/quotes/{self.author_id}.{name_to_goodreads(self.author_name)}'
        search = True

        while search:
            # Didn't found any quotes
            search = False
            # Navigate through the next page
            href_page = href + self._next_page(npage=npage)
            soup = self.connect(href=href_page)
            npage += 1
            for quote_div in scrape.scrape_quotes(soup):
                # Quotes found
                search = True
                quote_text = process_quote_text(scrape.get_quote_text(quote_div))
                quote_likes = eval(scrape.get_quote_likes(quote_div).text.replace('likes', '').strip())
                quote_href = scrape.get_quote_likes(quote_div).get('href')
                quote_id = quote_href.split('-')[0].split('.')[0]
                quote_tags = []
                for tag in scrape.scrape_quote_tags(quote_div):
                    quote_tags.append(tag.text.strip())
                quote = greads.Quote(self.author_id,
                                     quote_id,
                                     text=quote_text,
                                     author_name=self.author_name,
                                     tags=quote_tags,
                                     likes=quote_likes)
                # Register the quote to a book if it exists
                book_title = scrape.get_quote_book(quote_div)
                # The quote is linked to a book
                if book_title:
                    book_href = book_title.get('href')
                    book_id = book_href.split('/')[-1].split('-')[0].split('.')[0]
                    book_name = book_title.text.strip()
                    # Look for an already saved book, if it does not exists create it and add it
                    # However, if there are no books register using the ``search_book()`` method will automatically
                    # look for ALL books, which is time consuming.
                    # Instead, it will look for book already saved in the cache, and add it if it does not exist.
                    book_exist = True if book_id in [book.book_id for book in self._books] else False
                    if book_exist:
                        book = self.search_book(book_id)
                    else:
                        book = greads.Book(self.author_id, book_id, book_name=book_name, author_name=self.author_name)
                        self.add_book(book)
                    book.add_quote(quote)
                # Add the quote and return it
                self.add_quote(quote)
                yield quote

    def quotes(self, cache=True):
        """Yield all quotes from an author address.
        This function extract online data from `Good Reads` if nothing is already saved in the cache.

        Args:
            cache (bool): if ``True``, will look for cache items only (and won't scrape online).

        Returns:
            yield Quote

        """
        if len(self._quotes) > 0 and cache:
            yield from self._quotes
        else:
            yield from self._search_quotes()

    # TODO: merge this function with Book.get_quotes()
    def get_quotes(self, lang=None, top_k=None, cache=True):
        """Get all quotes from an author address.

        Args:
            lang (string): language to pick up quotes.
            top_k (int): number of quotes to retrieve (ordered by popularity).
            cache (bool): if ``True``, will look for cache items only (and won't scrape online).

        Returns:
            list(Quote)

        """
        # Reset the quotes saved in the cache if its length is under the threshold
        if top_k and len(self._quotes) < top_k:
            self._quotes = []
        # Get the top-k quotes, ordered from the author's quote page (usually it's ordered by popularity)
        quotes = []
        for i, quote in enumerate(self.quotes(cache=cache)):
            if not lang or langdetect.detect(quote.text) == lang:
                quote.register_author(self)
                quotes.append(quote)
                if top_k and i + 1 >= top_k:
                    break
        return quotes

    def books(self, cache=True):
        """Get all books from an author address.
        This function extract online data from `Good Reads` if nothing is already saved in the cache.

        Args:
            cache (bool): if ``True``, will look for cache items only (and won't scrape online).

        Returns:
            yield Quote

        """
        if len(self._books) > 0 and cache:
            yield from self._books
        else:
            yield from self._search_books()

    def get_books(self, top_k=None, cache=True):
        """Get all books from an author address.

        Args:
            top_k (int): number of books to return.
            cache (bool): if ``True``, will look for cache items only (and won't scrape online).

        Returns:
            list(Book)

        """
        # Reset the books saved in the cache if its length is under the threshold
        if top_k and len(self._books) < top_k:
            self._books = []
        # Get the top-k books, ordered from the author's book page
        books = []
        for i, book in enumerate(self.books(cache=cache)):
            book.register_author(self)
            books.append(book)
            if top_k and i + 1 >= top_k:
                break
        return books

    # TODO: use for loop with yield
    def search_book(self, book_id, attr='book_id', cache=True):
        """Search a book from the books saved in the author's cache.

        Args:
            book_id (string): book id (or name) to look for.
            attr (string, optional): attribute to search the book from. Options are ``'book_id'`` and ``'book_name'``
            cache (bool): if ``True``, will look for cache items only (and won't scrape online).

        Returns:
            Book

        """
        for book in self.books(cache=cache):
            if str(book_id) == str(getattr(book, attr)):
                book.register_author(self)
                return book

    # TODO: use for loop with yield
    def search_quote(self, quote_id, attr='quote_id', cache=True):
        """Search a quote from the books saved in the author's cache.

        Args:
            quote_id (string): quote'id to look for.
            attr (string, optional): attribute to search the quote from. Options are ``'quote_id'`` and ``'quote_name'``
            cache (bool): if ``True``, will look for cache items only (and won't scrape online).

        Returns:
            Book

        """
        for quote in self.quotes(cache=cache):
            if str(quote_id) == str(getattr(quote, attr)):
                quote.register_author(self)
                return quote

    def get_similar_authors(self, top_k=None):
        """Get similar artists from the author.

        Args:
            top_k (int): number of authors to retrieve (ordered by popularity).

        Returns:
            list(Author)

        """
        href = f'/author/similar/{self.author_id}.{name_to_goodreads(self.author_name)}'
        soup = self.connect(href=href)

        authors = []
        authors_container = soup.findAll('a', attrs={'class': 'gr-h3 gr-h3--serif gr-h3--noMargin'})
        for i, author in enumerate(authors_container[1:]):
            url_author = author.attrs['href']
            authors.append(Author.from_url(url_author))
            if top_k and i + 1 >= top_k:
                break
        return authors

    # TODO: finish and add nested JSON option
    def to_json(self, encode=None):
        """Encode the author to a JSON format.

        Args:
            encode (string): encode to ASCII format or not.

        Returns:
            dict

        """
        data = {
            'author': self.author_name,
            **self.get_info()
        }
        if encode:
            return serialize_dict(data)
        return data
