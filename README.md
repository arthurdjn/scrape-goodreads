# scrape-goodreads
Python package to scrape data from goodreads.com website. Authors, Books, and Quotes can be extracted.

*Project made during a Deep Learning project for music generation using GPT2 model.*


# Installation

Install *scrapereads* package from *PyPi*:

```
pip install scrapereads
```

Or from *GitHub*:

```
git clone https://github.com/arthurdjn/scrape-goodreads
cd scrape-goodreads
pip install .
```

# Getting Started

## GoodReads API

You can search for ``Author``, ``Book`` or ``Quote`` from the API:

```python
from scrapereads import GoodReads

# Connect to the API
goodreads = GoodReads()

# Search for an author, from it's ID.
AUTHOR_ID = 3389
author = goodreads.search_author(AUTHOR_ID)
# Search for a book
BOOK_ID = 3048970
book = goodreads.search_book(AUTHOR_ID, BOOK_ID)
# Look for the 10 first books (set it to ``top_k=None`` to turn it off)
books = goodreads.search_books(AUTHOR_ID, top_k=10)
# ...Or quotes
quotes = goodreads.search_quotes(AUTHOR_ID, top_k=10)
```

## Structure

The package is divided as follows:

* Author
* Book, inherits from Author
* Quote, inherits from Book


## Retrieve data


Once you have one of these objects, you can also access data directly through their methods:

```python
author = goodreads.search_author(AUTHOR_ID)
books = author.get_books()
quotes = author.get_quotes()

# Idem from an book
book = goodreads.search_book(AUTHOR_ID, BOOK_ID)
quotes = book.get_quotes()
```

In addition, you can retrieve parent objects from children:

```python
author = goodreads.search_author(AUTHOR_ID)
quotes = author.get_quotes(top_k=10)
quote = quotes[0]

# Access to parent classes
book = quote.get_book()
author = quote.get_author()
```

You can scrape for description, links and other details information:

```python
author = goodreads.search_author(AUTHOR_ID)
info = author.get_info()  # description of the author (genre, description, references etc.)
```

## Save and export

You can save data in a JSON format (and encode it to ASCII if you want).

```python
author = goodreads.search_author(AUTHOR_ID)
author_data = author.to_json(encode='ascii')
# Idem for book and quote
```

