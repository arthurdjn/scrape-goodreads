"""
Scrape quotes, books and authors from ``Good Reads`` website.
"""

import bs4
from .utils import *


def get_author_name(soup):
    """Get the author's name from its main page.

    Args:
        soup (bs4.element.Tag): connection to the author page.

    Returns:
        string: name of the author.

    Examples::
        >>> from scrapereads import connect
        >>> url = 'https://www.goodreads.com/author/show/1077326'
        >>> soup = connect(url)
        >>> get_author_name(soup)
            J.K. Rowling

    """
    author_h1 = soup.find('h1', attrs={'class': 'authorName'})
    return author_h1.find('span').text


def get_author_desc(soup):
    """Get the author description / biography.

    Args:
        soup (bs4.element.Tag): connection to the author page.

    Returns:
        str: long description of the author.

    Examples::
        >>> from scrapereads import connect
        >>> url = 'https://www.goodreads.com/author/show/1077326'
        >>> soup = connect(url)
        >>> get_author_desc(soup)
            See also: Robert Galbraith
            Although she writes under the pen name J.K. Rowling, pronounced like rolling,
            her name when her first Harry Potter book was published was simply Joanne Rowling.
            ...

    """
    author_info_desc = soup.find('div', attrs={'class': 'aboutAuthorInfo'})
    author_info_long = author_info_desc.findAll('span')[-1]
    long_desc = ""
    for sentence in author_info_long.children:
        if isinstance(sentence, bs4.element.Tag):
            if sentence.name == 'br':
                long_desc += '\n'
            else:
                long_desc += sentence.text
        else:
            long_desc += sentence
    long_desc = long_desc.replace('’', "'")
    return long_desc


def get_author_info(soup):
    """Get all information from an author (genres, influences, website etc.).

    Args:
        soup (bs4.element.Tag): author page connection.

    Returns:
        dict

    """
    container = soup.find('div', attrs={'class': 'rightContainer'})
    author_info = {}
    data_div = container.find('br', attrs={'class': 'clear'})
    while data_div:
        if data_div.name:
            data_class = data_div.get('class')[0]
            # Information section is finished
            if data_class == 'aboutAuthorInfo':
                break
            # Key elements
            elif data_class == 'dataTitle':
                key = data_div.text.strip()
                author_info[key] = []
            # Born section
            if data_div.text == 'Born':
                data_div = data_div.next_sibling
                author_info[key].append(data_div.strip())
            # Influences section
            elif data_div.text == 'Influences':
                data_div = data_div.next_sibling.next_sibling
                data_items = data_div.findAll('span')[-1].findAll('a')
                for data_a in data_items:
                    author_info[key].append(data_a.text.strip())
            # Member since section
            elif data_div.text == 'Member Since':
                data_div = data_div.next_sibling.next_sibling
                author_info[key].append(data_div.text.strip())
            # Genre, website and other sections
            else:
                data_items = data_div.findAll('a')
                for data_a in data_items:
                    author_info[key].append(data_a.text.strip())
        data_div = data_div.next_sibling
    author_info.update({'Description': get_author_desc(soup)})
    return author_info


def scrape_quotes_container(soup):
    """Get the quote container from a quote page.

    Args:
        soup (bs4.element.Tag): connection to the quote page.

    Returns:
        bs4.element.Tag

    """
    return soup.findAll('div', attrs={'class': 'quotes'})


def scrape_quotes(soup):
    """Retrieve all ``<div>`` quote element from a quote page.

    Args:
        soup (bs4.element.Tag): connection to the quote page.

    Returns:
        yield bs4.element.Tag

    """
    for container_div in scrape_quotes_container(soup):
        quote_div = container_div.find('div', attrs={'class': 'quote'})
        while quote_div:
            if quote_div.name == 'div' and quote_div.get('class') and 'quote' in quote_div.get('class'):
                yield quote_div
            quote_div = quote_div.next_sibling


def get_quote_text(quote_div):
    """Get the text from a ``<div>`` quote element.

    Args:
        quote_div (bs4.element.Tag): ``<div>`` quote element to extract the text.

    Returns:
        string

    """
    quote_text = ''
    text_iterator = quote_div.find('div', attrs={'class': 'quoteText'}).children
    for text in text_iterator:
        if text.name == 'br':
            quote_text += '\n'
        elif not text.name:
            quote_text += text.strip()
    quote_text = process_quote_text(quote_text)
    return quote_text


def scrape_quote_tags(quote_div):
    """Scrape tags from a ``<div>`` quote element.

    Args:
        quote_div (bs4.element.Tag): ``<div>`` quote element from a quote page.

    Returns:
        yield ``<a>`` tags

    """
    tags_container = quote_div.find('div', attrs={'class': 'greyText smallText left'})
    if tags_container:
        for tag in tags_container.children:
            if tag.name == 'a':
                yield tag
    return None


def get_quote_book(quote_div):
    """Get the reference (book) from a ``<div>`` quote element.

    Args:
        quote_div (bs4.element.Tag): ``<div>`` quote element from a quote page.

    Returns:
        bs4.element.Tag

    """
    quote_details = quote_div.find('div', attrs={'class': 'quoteText'})
    return quote_details.find('a', attrs={'class': 'authorOrTitle'})


def get_quote_author_name(quote_div):
    """Get the author's name from a ``<div>`` quote element.

    Args:
        quote_div (bs4.element.Tag): ``<div>`` quote element from a quote page.

    Returns:
        string

    """
    quote_text = quote_div.find('div', attrs={'class': 'quoteText '})
    author_name = quote_text.find('span', attrs={'class': 'authorOrTitle'}).text
    return remove_punctuation(author_name).title()


def get_quote_likes(quote_div):
    """Get the likes ``<a>`` tag from a ``<div>`` quote element.

    Args:
        quote_div (bs4.element.Tag): ``<div>`` quote element from a quote page.

    Returns:
        bs4.element.Tag: ``<a>`` tag for likes.

    """
    quote_footer = quote_div.find('div', attrs={'class': 'quoteFooter'})
    return quote_footer.find('a', attrs={'class': 'smallText'})


# TODO: deprecate this
def get_quote_name_id(quote_div):
    """Get the name and id of a ``<div>`` quote element.

    Args:
        quote_div (bs4.element.Tag): ``<div>`` quote element from a quote page.

    Returns:
        tuple: id and name.

    """
    quote_href = get_quote_likes(quote_div).get('href')
    quote_id = quote_href.split('/')[-1].split('-')[0]
    quote_name = '-'.join(quote_href.split('/')[-1].split('-')[1:])
    return quote_id, quote_name


def scrape_author_books(soup):
    """Retrieve books from an author's page.

    Args:
        soup (bs4.element.Tag): connection to an author books page.

    Returns:
        yield bs4.element.Tag: ``<tr>`` element.

    """
    table_tr = soup.find('tr')
    while table_tr:
        if table_tr.name == 'tr':
            yield table_tr
        table_tr = table_tr.next_sibling


def get_author_book_title(book_tr):
    """Get the book title ``<a>`` element from a table ``<tr>`` element from an author page.

    Args:
        book_tr (bs4.element.Tag): ``<tr>`` book element.

    Returns:
        bs4.element.Tag: book title ``<a>`` element.

    Examples::
        >>> for book_tr in scrape_author_books(soup):
        ...     book_title = get_author_book_title(book_tr)
        ...     print(book_title.text.strip(), book_title.get('href'))
            The Bell Jar /book/show/6514.The_Bell_Jar
            Ariel /book/show/395090.Ariel
            The Collected Poems /book/show/31426.The_Collected_Poems
            The Unabridged Journals of Sylvia Plath /book/show/11623.The_Unabridged_Journals_of_Sylvia_Plath

    """
    return book_tr.find('a', attrs={'class': 'bookTitle'})


def get_author_book_author(book_tr):
    """Get the author ``<a>`` element from a table ``<tr>`` element.

    Args:
        book_tr (bs4.element.Tag): ``<tr>`` book element.

    Returns:
        bs4.element.Tag: author name ``<a>`` element.

    Examples::
        >>> for book_tr in scrape_author_books(soup):
        ...     book_author = get_author_book_author(book_tr)
        ...     print(book_author.text, book_author.get('href'))
            Sylvia Plath https://www.goodreads.com/author/show/4379.Sylvia_Plath
            Sylvia Plath https://www.goodreads.com/author/show/4379.Sylvia_Plath
            Sylvia Plath https://www.goodreads.com/author/show/4379.Sylvia_Plath
            Sylvia Plath https://www.goodreads.com/author/show/4379.Sylvia_Plath
            Sylvia Plath https://www.goodreads.com/author/show/4379.Sylvia_Plath

    """
    return book_tr.find('a', attrs={'class': 'authorName'})


def get_author_book_ratings(book_tr):
    """Get the ratings ``<span>`` element from a table ``<tr>`` element from an author page.

    Args:
        book_tr (bs4.element.Tag): ``<tr>`` book element.

    Returns:
        bs4.element.Tag: ratings ``<span>`` element.

    Examples::
        >>> for book_tr in scrape_author_books(soup):
        ...     ratings_span = get_author_book_ratings(book_tr)
        ...     print(ratings_span.contents[-1])
             4.55 avg rating — 2,414 ratings
             3.77 avg rating — 1,689 ratings
             4.28 avg rating — 892 ratings
             4.54 avg rating — 490 ratings
             ...

    """
    return book_tr.find('span', attrs={'class': 'minirating'})


def get_author_book_edition(book_tr):
    """Get the edition ``<a>`` element from a table ``<tr>`` element from an author page.

    Args:
        book_tr (bs4.element.Tag): ``<tr>`` book element.

    Returns:
        bs4.element.Tag: book edition ``<a>`` element.

    Examples::
        >>> for book_tr in scrape_author_books(soup):
        ...     book_edition = get_author_book_edition(book_tr)
        ...     if book_edition:
        ...         print(book_edition.text, book_edition.get('href'))
        ...         print()
            493 editions /work/editions/1385044-the-bell-jar
            80 editions /work/editions/1185316-ariel
            30 editions /work/editions/1003095-the-collected-poems
            45 editions /work/editions/3094683-the-unabridged-journals-of-sylvia-plath
            ...

    """
    book_details = book_tr.find('span', attrs={'class': 'greyText smallText uitext'})
    return book_details.find('a', attrs={'class': 'greyText'})


def get_author_book_date(book_tr):
    """Get the published date from a table ``<tr>`` element from an author page.

    Args:
        book_tr (bs4.element.Tag): ``<tr>`` book element.

    Returns:
        int: date of publication

    Examples::
        >>> for book_tr in scrape_author_books(soup):
        ...     book_date = get_author_book_date(book_tr)
        ...     print(book_date)
            None
            None
            1958
            2009
            ...

    """
    book_details = book_tr.find('span', attrs={'class': 'greyText smallText uitext'})
    book_publish = book_details.contents[-1].replace('—', '').replace('\n', '')
    book_date = book_publish.replace('published', '').strip()
    book_date = eval(book_date) if book_date != '' else None
    return book_date


def get_book_quote_page(soup):
    """Find the ``<a>`` element pointing to the quote page of a book.

    Args:
        soup (bs4.element.Tag):

    Returns:

    """
    quote_div = soup.findAll('div', attrs={'class': ' clearFloats bigBox'})
    if quote_div:
        return quote_div[-1].find('a')
    return None
