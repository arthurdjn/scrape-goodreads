# scrape-goodreads
Python package to scrape data from goodreads.com website. Authors, Books, and Quotes can be extracted.

*Project made during a Deep Learning project for poem generation using GPT2 model.*


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
quotes = goodreads.search_quotes(AUTHOR_ID, top_k=5)
```

Quotes are made of a text, but optional information can be added (like number of likes, tags,
reference etc.)

```python
quotes = goodreads.search_quotes(AUTHOR_ID, top_k=5)

for quote in quotes:
    print(quote)
    print()
```
Output:
```pycon
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

