"Auxilary url processing functions for page_loader.py."

import logging
from typing import Literal
import requests
from typing import Tuple, Union
from urllib.parse import urlparse


class KnownError(Exception):
    "Some known error."
    pass


def hyphenate(string: str) -> str:
    """Replace non-numeric and non-literal characters with a hyphen.

    Parameters:
        string: string to be processed.

    Returns:
        hyphenated string.
    """
    return ''.join([
        '-' if not i.isalpha() and not i.isdigit() else i for i in string
    ])


def _get_name(url: str) -> str:  # ru-hexlet-io-cources
    """Derive a name of a directory or file from an url.

    Parameters:
        url: webpage url.

    Returns:
        directory or file name as a string.
    """
    parsed = urlparse(str(url))
    address = parsed.netloc + parsed.path
    return hyphenate(address)


def get_directory_name(url: str) -> str:
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
    return hyphenate(parsed)


def get_html_file_name(url: str) -> str:  # ru-hexlet-io-cources.html
    """Get a name of a file containing downloaded webpage.

    Parameters:
        url: webpage url.

    Returns:
        name of a file containing the downloaded webpage.
    """
    return _get_name(url) + '.html'


def get_webpage_data(url: str) -> str:
    """Request data from a webpage.

    Parameters:
        url: webpage url.

    Returns:
        webpage contents.
    """
    try:
        request = requests.get(url)
        request.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        logging.error(exc)
        raise KnownError(f"Connection failed. \
Status code: {requests.get(url).status_code}") from exc
    return request.text


def get_resource_data(
    url: str,
    resource: str,
) -> Tuple[Union[str, bytes], str]:
    """Write 'link' or 'source' tags contents into file.

    Parameters:
        url: website url,
        resource: resource link.

    Returns:
        data from a resource.
    """
    resource_parse = urlparse(resource)
    if resource_parse.netloc:
        data = get_webpage_data(resource)
        flag = 'w'
    else:
        data = requests.get(url + resource).content
        flag = 'wb+'
    return data, flag


def prepare_url(url: str) -> str:
    """Get url in the form of scheme://netloc.

    Parameters:
        url: webpage url.

    Returns:
        url in the form of scheme://netloc.
    """
    parsed_url = urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.netloc


def is_local(url: str, webpage_url: str) -> Literal:
    """Check whether a resource is local or not.

    Parameters:
        url: url from src/href.

    Returns:
        true if local, false if not
    """
    parse_result = urlparse(str(url))
    webpage_netloc = urlparse(webpage_url).netloc
    return parse_result.netloc == webpage_netloc or parse_result.netloc == ''
