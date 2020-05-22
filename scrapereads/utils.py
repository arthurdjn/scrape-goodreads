"""
Functional functions to process names and data.
"""

import re
import string


CHARS = [
    ('-', ''),
    (' ', '_'),
    ('/', ''),
    ('.', ''),
    (',', ''),
    ("'", ''),
    ("`", ''),
    ("&", ''),
    ('?', ''),
    ("!", ''),
    ('.', ''),
]

HTML = [
    ('<br/>', ''),
    ('<br>', ''),
    ('<i>', ''),
    ('</i>', ''),
    ('<b>', ''),
    ('</b>', ''),
    ('”', ''),
    ('“', ''),
    ('’', "'"),
]


ROMAN_MAP = [
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I')
]


def name_to_goodreads(name):
    """Process and convert names in scrapereads format.

    Args:
        name (string): name of an author.

    Returns:
        string

    """
    name = to_ascii(name.title())
    for char in CHARS:
        name = name.replace(*char)
    return name


def num2roman(num):
    """Convert a number to roman's format.

    Args:
        num (int): number to convert.

    Returns:
        string

    """
    roman = ''
    while num > 0:
        for i, r in ROMAN_MAP:
            while num >= i:
                roman += r
                num -= i
    return roman


ROMAN = [(f" {num2roman(k)} ", "") for k in range(2, 30)] + \
        [(f" {num2roman(k).lower()} ", "") for k in range(2, 30)]
ROMAN += [(f" {num2roman(k)}\n", "\n") for k in range(2, 30)] + \
         [(f" {num2roman(k).lower()}\n", "\n") for k in range(2, 30)]
ROMAN += [(f"\n{num2roman(k)} ", "\n") for k in range(2, 30)] + \
         [(f"\n{num2roman(k).lower()} ", "\n") for k in range(2, 30)]


def clean_num(quote):
    """Remove romans numbers from a quote.

    Args:
        quote (string): quote.

    Returns:
        string

    """
    for char in ROMAN:
        quote = quote.replace(*char)
    return quote


def to_ascii(text):
    """Convert a text to ASCII format.

    Args:
        text (string): text to process.

    Returns:
        string

    """
    return re.sub(r'[^\x00-\x7F]+', ' ', text)


def process_quote_text(quote_text):
    """Clean up the text from a ``<div>`` quote element.

    Args:
        quote_text (string): quote text to clean.

    Returns:
        string

    """
    quote_text = quote_text.replace('―', '').replace('\n\n', '\n')
    quote_text = quote_text[:-1] if quote_text[-1] == '\n' else quote_text
    for char in HTML:
        quote_text = quote_text.replace(*char)
    return quote_text


def remove_punctuation(string_punct):
    """Remove punctuation from a string.

    Args:
        string_punct (string): string with punctuation.

    Returns:
        string

    """
    return string_punct.translate(str.maketrans('', '', string.punctuation))


def parse_author_href(href):
    """Split an href and retrieve the author's name and its key.

    Args:
        href (string): ``Good Reads`` href pointing to an author page.

    Returns:
        tuple: author's name and key.

    """
    author_parts = href.split('/')[-1].split('.')
    key = author_parts[0]
    author_name = author_parts[1].replace('_', ' ')
    return author_name, key


import unidecode


def serialize_list(list_raw):
    """Serialize a list in ASCII format, so it can be saved as a JSON.

    Args:
        list_raw (list):

    Returns:
        list

    """
    list_serialized = []
    for value in list_raw:
        if isinstance(value, list):
            list_serialized.append(serialize_list(value))
        elif isinstance(value, dict):
            list_serialized.append(serialize_dict(value))
        else:
            list_serialized.append(unidecode.unidecode(str(value)))
    return list_serialized


def serialize_dict(dict_raw):
    """Serialize a dictionary in ASCII format so it can be saved as a JSON.

    Args:
        dict_raw (dict):

    Returns:
        dict

    """
    dict_serialized = {}
    for (key, value) in dict_raw.items():
        if isinstance(value, list):
            dict_serialized[unidecode.unidecode(str(key))] = serialize_list(value)
        elif isinstance(value, dict):
            dict_serialized[unidecode.unidecode(str(key))] = serialize_dict(value)
        else:
            dict_serialized[unidecode.unidecode(str(key))] = unidecode.unidecode(str(value))
    return dict_serialized


def serialize_list(list_raw):
    """Serialize a list in ASCII format, so it can be saved as a JSON.

    Args:
        list_raw (list):

    Returns:
        list

    """
    list_serialized = []
    for value in list_raw:
        if isinstance(value, list):
            list_serialized.append(serialize_list(value))
        elif isinstance(value, dict):
            list_serialized.append(serialize_dict(value))
        else:
            list_serialized.append(unidecode.unidecode(str(value)))
    return list_serialized


def serialize_dict(dict_raw):
    """Serialize a dictionary in ASCII format so it can be saved as a JSON.

    Args:
        dict_raw (dict):

    Returns:
        dict

    """
    dict_serialized = {}
    for (key, value) in dict_raw.items():
        if isinstance(value, list):
            dict_serialized[unidecode.unidecode(str(key))] = serialize_list(value)
        elif isinstance(value, dict):
            dict_serialized[unidecode.unidecode(str(key))] = serialize_dict(value)
        else:
            dict_serialized[unidecode.unidecode(str(key))] = unidecode.unidecode(str(value))
    return dict_serialized
