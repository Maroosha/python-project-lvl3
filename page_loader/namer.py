"Auxilary naming functions for page_loader.py."

import logging
from urllib.parse import urlparse


def _get_name(url):  # ru-hexlet-io-cources
    """Derive a name of a directory or file from an url.

    Parameters:
        url: webpage url.

    Returns:
        directory or file name as a string.
    """
    parsed = urlparse(str(url))
    address = parsed.netloc + parsed.path
    name = [
        '-' if not i.isalpha() and not i.isdigit() else i for i in address
    ]
    return ''.join(name)


def get_directory_name(url):
    """Get directory name containing downloaded webpage data.

    Parameters:
        url: webpage url.

    Returns:
        directory name as a string.
    """
    return _get_name(url) + '_files'


def get_website_name(url: str) -> str:  # ru-hexlet-io
    """Get a name of a file containing downloaded webpage.

    Parameters:
        url: webpage url.

    Returns:
        name of a file containing the downloaded webpage.
    """
    parsed = urlparse(str(url)).netloc
    name = [
        '-' if not i.isalpha() and not i.isdigit() else i for i in parsed
    ]
    logging.debug(f'Website name: {"".join(name)}')
    return ''.join(name)


def get_html_file_name(url: str) -> str:  # ru-hexlet-io-cources.html
    """Get a name of a file containing downloaded webpage.

    Parameters:
        url: webpage url.

    Returns:
        name of a file containing the downloaded webpage.
    """
    return _get_name(url) + '.html'
