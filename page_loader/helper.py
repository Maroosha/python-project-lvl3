"Helper functions for page_loader.py."

import logging
import requests
from urllib.parse import urlparse


class KnownError(Exception):
    "Some known error."
    pass


def get_name(url):  # ru-hexlet-io-cources
    """Derive a name of a directory or file from an url.

    Parameters:
        url: webpage url.

    Returns:
        directory or file name as a string.
    """
    address = url.split('//')[1]
    name = [
        '-' if not i.isalpha() and not i.isdigit() else i for i in address
    ]
    return ''.join(name)


def get_directory_name(name):  # ru-hexlet-io-cources_files
    """Get directory name containing downloaded webpage data.

    Parameters:
        name: name derived from url.

    Returns:
        directory name as a string.
    """
    return name + '_files'


def get_website_name(url):  # ru-hexlet-io
    """Get a name of a file containing downloaded webpage.

    Parameters:
        name: name derived from url.

    Returns:
        name of a file containing the downloaded webpage.
    """
    address = url.split('//')[1].split('/')[0]
    name = [
        '-' if not i.isalpha() and not i.isdigit() else i for i in address
    ]
    logging.debug(f'Website name: {"".join(name)}')
    return ''.join(name)


def get_main_file_name(name):  # ru-hexlet-io-cources.html
    """Get a name of a file containing downloaded webpage.

    Parameters:
        name: name derived from url.

    Returns:
        name of a file containing the downloaded webpage.
    """
    return name + '.html'


def get_webpage_contents(url):
    """Request data from a webpage.

    Parameters:
        url: webpage url.

    Returns:
        webpage content.
    """
    try:
        request = requests.get(url)
        request.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        logging.error(exc)
        raise KnownError(f"Connection failed. \
Status code: {requests.get(url).status_code}") from exc
    return request.text


def prepare_url(url):
    """Get url in the form of scheme://netloc.

    Parameters:
        url: webpage url.

    Returns:
        url in the form of scheme://netloc.
    """
    parsed_url = urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.netloc


def write_to_file(filepath, webpage_content):
    """Write webpage content to file.

    Parameters:
        url: webpage url,
        filepath: path to file.
    """
    try:
        with open(filepath, 'w') as file_:
            file_.write(webpage_content)
    except PermissionError as error1:
        print(f'Access denied to file {filepath}.')
        logging.error('Access denied to file %s.', filepath)
        raise error1
    except OSError as error2:
        print(f'Unable to write to file {filepath}.')
        logging.error('Unable to write to file %s.', filepath)
        raise error2


def is_local(url, webpage_url):
    """Check whether a resource is local or not
    (if it belongs to ru.hexlet.io).

    Parameters:
        url: url from src/href.

    Returns:
        true if local, false if not
    """
    parse_result = urlparse(str(url))
    webpage_netloc = urlparse(webpage_url).netloc
    return parse_result.netloc == webpage_netloc or parse_result.netloc == ''
