========
Examples
========

The requests should be made from the API. Then, you can have access to authors, books, quotes.


LyricsFandom API
================

The API uses ``id`` to search authors, books or quotes.

.. code-block:: python

    from scrapereads import GoodReads

    # Connect to the API
    goodreads = GoodReads()
    # Examples
    # Author id: 3389    -> Stephen King
    #            1077326 -> J. K. Rolling
    AUTHOR_ID = 3389
    author = goodreads.search_author(AUTHOR_ID)


You can have access to their attributes with:

.. code-block:: python

    # From an Author
    author_name = author.author_name
    author_id = author.author_id

    # From a Book
    author_name = book.author_name
    author_id = book.author_id
    book_name = book.book_name
    book_id = book.book_id
    edition = book.edition
    year = book.year
    ratings = book.ratings

    # From a Quote
    author_name = quote.author_name
    author_id = quote.author_id
    quote_id = quote.quote_id
    tags = quote.tags
    likes = quote.likes


Access data
===========

Once you have an object instance, you can retrieve data:

.. code-block:: python

    # From an Author
    AUTHOR_ID = 3389
    author = goodreads.search_author(AUTHOR_ID)
    books = author.get_books(top_k=None)
    quotes = author.get_quotes(top_k=None)

    # From a Book
    BOOK_ID = 3048970
    book = goodreads.search_book(AUTHOR_ID, BOOK_ID)
    quotes = book.get_quotes()


Note:

If you want to navigate through books, quotes, you may prefer using ``.quotes()`` or ``.books()`` methods,
which yields items successively and thus are more optimized as all items are not loaded directly.

.. code-block:: python

    # From and author
    author = goodreads.search_author(AUTHOR_ID)
    for quote in author.quotes():
        lyrics = quote.get_lyrics()
        print(lyrics)
        print('\n-----\n')


From children classes (author --> book --> quote), you can retrieve data too:

.. code-block:: python

    author = goodreads.search_author(AUTHOR_ID)
    quotes = author.get_quotes(top_k=5)
    books = author.get_books(top_k=5)

    # From a quote
    quote = quotes[0]
    book = quote.get_book()
    author = quote.get_author()

    # From an book
    book = books[0]
    author = book.get_author()


Save and export
===============

You can save all classes with the ``.to_json()`` method. The ``'ascii'`` argument will transforms all string to
ASCII format. If you don't want it, just remove it.

.. code-block:: python

    # From an author
    author = goodreads.search_author(AUTHOR_ID)
    author_data = author.to_json(encode='ascii')
    # Or directly
    author_data = goodreads.get_author(AUTHOR_ID, encode='ascii')

    # From an book
    book = goodreads.search_book(AUTHOR_ID, BOOK_ID)
    book_data = book.to_json(encode='ascii')
    # Or directly
    book_data = goodreads.get_books(AUTHOR_ID, top_k=NUMBER, encode=None)

    # From a quote
    quote_data = quote.to_json(encode='ascii')
    # Or directly
    quote_data = goodreads.get_quotes(AUTHOR_ID, top_k=NUMBER, encode=None)


