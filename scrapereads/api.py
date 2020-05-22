"""
Simple API to connect and extract data from ``Good Reads`` servers.
"""

from .connect import *
from .reads import Author, Book, Quote


class GoodReads:
    """Main API for `Good Reads` scrapping.

        It basically wraps ``Author``, ``Book`` and ``Quote`` classes.

        """

    def __init__(self, verbose=False, sleep=0, user=None):
        super().__init__()
        self.set_user(user)
        self.set_verbose(verbose)
        self.set_sleep(sleep)

    @staticmethod
    def set_user(user):
        """Change the user agent used to connect on internet.

        Args:
            user (string): user agent to use with urllib.request.

        """
        set_user(user)

    @staticmethod
    def set_verbose(verbose):
        """Change the log / display while surfing on internet.

        Args:
            verbose (bool): if ``True`` will display a log message each time it is connected to a page.

        """
        set_verbose(verbose)

    @staticmethod
    def set_sleep(sleep):
        """Time before connecting again to a new page.

        Args:
            sleep (float): seconds to wait.

        """
        set_sleep(sleep)

    @staticmethod
    def search_author(author_id):
        """Search an author from `Good Reads` server.

        Args:
            author_id (string): name of the author to get.

        Returns:
            Author

        """
        author = Author(author_id)
        return author

    @staticmethod
    def search_book(author_id, book_id):
        """Search an book from `Good Reads` server.

        Args:
            author_id (string): name of the author who made the book.
            book_id (string): name of the book.

        Returns:
            Book

        """
        author = Author(author_id)
        return author.search_book(book_id)

    @staticmethod
    def search_books(author_id, top_k=10):
        """Search books in from an author.

        Args:
            author_id (string): name of the author to get.
            top_k (int): number of books to retrieve.

        Returns:
            list(Book)

        """
        author = Author(author_id)
        return author.get_books(top_k=top_k)

    @staticmethod
    def search_quotes(author_id, top_k=50):
        """Search quotes from `Good Reads` server.

        Args:
            author_id (string): name of the author who made the quote.
            top_k (int): number of quotes to retrieve.

        Returns:
            Quote

        """
        author = Author(author_id)
        return author.get_quotes(top_k=top_k)

    @staticmethod
    def search_query(query):
        raise NotImplementedError

    @staticmethod
    def get_author(author_id, encode=None):
        """Get an author in a JSON format.

        Args:
            author_id (string): name of the author.
            encode (string): encode to ASCII format or not.

        Returns:
            dict

        """
        author = Author(author_id)
        return author.to_json(encode=encode)

    @staticmethod
    def get_quotes(author_id, top_k=10):
        """Get all quotes in a JSON format from an author.

        Args:
            author_id (string): name of the author to get.
            top_k (int): number of quotes to retrieve.

        Returns:
            list(dict)

        """
        author = Author(author_id)
        quotes = []
        for i, quote in enumerate(author.quotes()):
            quotes.append(quote.to_json())
            if top_k and i + 1 >= top_k:
                return quotes
        return quotes

    @staticmethod
    def get_books(author_id, top_k=10):
        """Get all books in a JSON format from an author.

        Args:
            author_id (string): name of the author to get.
            top_k (int): number of books to retrieve.

        Returns:
            list(dict)

        """
        author = Author(author_id)
        books = []
        for i, book in enumerate(author.books()):
            books.append(book.to_json())
            if top_k and i + 1 >= top_k:
                return books
        return books
