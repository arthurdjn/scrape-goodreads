===============
Getting Started
===============


Installation
============


Install *scrapereads* package from *PyPi*:

.. code-block:: pycon

    pip install scrapereads


Or from *GitHub*:

.. code-block:: pycon

    git clone https://github.com/arthurdjn/scrape-goodreads
    cd scrape-goodreads
    pip install .


Usage
=====

You can use the simplified API to look for books and quotes.

Example:

.. code-block:: python

    from scrapereads import GoodReads

    # Connect to the API
    goodreads = GoodReads()
    # Search for an author, by its id.
    AUTHOR_ID = 3389
    author = goodreads.search_author(3389)
    author


Output:

.. code-block:: pycon

    Author: Stephen King


Then, you can search for book(s) too. Use ``top_k=NUMBER`` to look for an amount of books.

Example:

.. code-block:: python

    # Search for books
    # Will look for the first 5 books
    books = goodreads.search_books(AUTHOR_ID, top_k=5)
    books


Output:

.. code-block:: pycon

    [Stephen King: "The Shining", 387 editions,
     Stephen King: "It", 313 editions,
     Stephen King: "The Stand", 230 editions,
     Stephen King: "Misery", 263 editions,
     Stephen King: "Carrie", 315 editions]


Finally, you can scrape for quotes.

Example:

.. code-block:: python

    # Search for quotes
    quotes = goodreads.search_quotes(AUTHOR_ID, top_k=5)

    for quote in quotes:
        print(quote)
        print()


Output:

.. code-block:: pycon

    “Books are a uniquely portable magic.”
    ― Stephen King, from "On Writing: A Memoir Of The Craft"
      Likes: 16225, Tags: books, magic, reading

    “If you don't have time to read, you don't have the time (or the tools) to write. Simple as that.”
    ― Stephen King
      Likes: 12565, Tags: reading, writing

    “Get busy living or get busy dying.”
    ― Stephen King, from "Different Seasons"
      Likes: 9014, Tags: life

    “Books are the perfect entertainment: no commercials, no batteries, hours of enjoyment for each dollar spent. What I wonder is why everybody doesn't carry a book around for those inevitable dead spots in life.”
    ― Stephen King
      Likes: 8667, Tags: books

    “When his life was ruined, his family killed, his farm destroyed, Job knelt down on the ground and yelled up to the heavens, "Why god? Why me?" and the thundering voice of God answered, There's just something about you that pisses me off.”
    ― Stephen King, from "Storm Of The Century"
      Likes: 7686, Tags: god, humor, religion


