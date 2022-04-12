"Auxilary in-out functions for page_loader.py."

import logging
import requests
import page_loader.url as url_
from typing import Union


def write_to_file(filepath: str, data: Union[bytes, str]):
    """Write webpage content to file.

    Parameters:
        filepath: path to file,
        data: data to be written to file.
    """
    format = 'wb+' if isinstance(data, bytes) else 'w'
    try:
        with open(filepath, format) as file_:
            file_.write(data)
    except PermissionError as error1:
        logging.error('Access denied to file %s.', filepath)
        raise error1
    except OSError as error2:
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
        raise url_.KnownError(f"Connection failed. \
Status code: {requests.get(url).status_code}") from exc
    return request.content


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
    link = url_.to_absolute(url, resource)
    return get_webpage_data(link)
