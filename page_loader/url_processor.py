"Auxilary url processing functions for page_loader.py."

import logging
#  import os
from typing import Literal
import requests
from urllib.parse import urlparse


class KnownError(Exception):
    "Some known error."
    pass


def get_webpage_contents(url: str) -> str:
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
