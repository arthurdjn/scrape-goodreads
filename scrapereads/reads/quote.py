"""
Defines a quote from an Author.
"""

from abc import ABC, abstractmethod
import langdetect

from scrapereads.connect import connect
from scrapereads.utils import *
from scrapereads.meta import QuoteMeta


class Quote(QuoteMeta):
    """Defines a quote from the quote page from ``https://www.goodreads.com/author/quotes/``.

    """

    def __init__(self, author_id, quote_id, text='', quote_name=None, author_name=None, tags=None, likes=None):
        super().__init__(author_id, quote_id, text=text, quote_name=quote_name, author_name=author_name, tags=tags,
                         likes=likes)

    # TODO: add nested JSON option
    def to_json(self, encode='ascii'):
        """Encode the quote to a JSON format.

        Returns:
            dict

        """
        book = self.get_book()
        book_name = None
        if book:
            book_name = book.book_name

        # Default data, without any encoding
        data = {
            'author': self.author_name,
            'book': book_name,
            'likes': self.likes,
            'tags': self.tags,
            'quote': self.text,
        }
        if encode:
            return serialize_dict(data)
        return data