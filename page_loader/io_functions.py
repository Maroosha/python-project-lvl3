"Auxilary in-out functions for page_loader.py."

import logging
import requests
from page_loader.url import KnownError
from typing import Union
from urllib.parse import urlparse


def write_to_file(filepath: str, data: Union[bytes, str]):
    """Write webpage content to file.

    Parameters:
        filepath: path to file,
        data: data to be written to file.
    """
    try:
        if isinstance(data, bytes):
            with open(filepath, 'wb+') as file_:
                file_.write(data)
        else:
            with open(filepath, 'w') as file_:
                file_.write(data)
    except PermissionError as error1:
        print(f'Access denied to file {filepath}.')
        logging.error('Access denied to file %s.', filepath)
        raise error1
    except OSError as error2:
        print(f'Unable to write to file {filepath}.')
        logging.error('Unable to write to file %s.', filepath)
        raise error2


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
) -> Union[bytes, str]:
    """Write 'img', 'link' or 'source' tags contents into file.

    Parameters:
        url: website url,
        resource: resource link.

    Returns:
        data from a resource.
    """
    resource_parse = urlparse(resource)
    if resource_parse.netloc:
        data = get_webpage_data(resource)
    else:
        data = requests.get(url + resource).content
    return data
