"""
Defines a book from an Author.
"""

import warnings
import langdetect

from scrapereads.utils import *
from scrapereads import scrape
from scrapereads.meta import BookMeta
import scrapereads.reads as greads


class Book(BookMeta):
    def __init__(self, author_id, book_id, book_name=None, author_name=None, edition=None, year=None,
                 ratings=None):
        super().__init__(author_id, book_id, book_name=book_name, author_name=author_name, edition=edition,
                         year=year)
        self.ratings = ratings
        self._quotes = []

    def _search_quotes(self):
        # Scrape online quotes from goodreads.com
        self._quotes = []
        soup = self.connect()
        href_a = scrape.get_book_quote_page(soup)
        if href_a:
            href = href_a.get('href')
            npage = 1
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
                    self.add_quote(quote)
                    yield quote

    def quotes(self, cache=True):
        """Yield all quotes from a book address.
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

    def get_quotes(self, lang=None, top_k=None, cache=True):
        """Get all quotes from a book address.

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
        # Get the top-k quotes, ordered from the book's quote page (usually it's ordered by popularity)
        quotes = []
        for i, quote in enumerate(self.quotes(cache=cache)):
            if not lang or langdetect.detect(quote.text) == lang:
                quote.register_book(self)
                quotes.append(quote)
                if top_k and i + 1 >= top_k:
                    break
        return quotes

    def add_quote(self, quote):
        """Add a quote to the Book, that will be saved in the cache.

        Args:
            quote (Quote): quote to add.

        """
        quote.author_name = self.author_name
        quote.author_id = self.author_id
        quote.register_author(self.get_author())
        quote.register_book(self)
        self._quotes.append(quote)

    # TODO: add nested JSON option
    def to_json(self, encode='ascii'):
        """Encode the book to a JSON format.

        Returns:
            dict

        """

        # Default data, without any encoding
        data = {
            'author': self.author_name,
            'book': self.book_name,
            'edition': self.edition,
            'year': self.year,
            'quotes': [],
        }
        for quote in self.quotes():
            data['quotes'].append(quote.to_json(encode=encode))
        if encode:
            return serialize_dict(data)
        return data
