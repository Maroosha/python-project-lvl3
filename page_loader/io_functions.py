"Auxilary in-out functions for page_loader.py."

import logging
import requests
import page_loader.url_processor as urlproc
from urllib.parse import urlparse


def write_to_file(filepath: str, data: str):
    """Write webpage content to file.

    Parameters:
        filepath: path to file,
        data: data to be written to file.
    """
    try:
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


def write_resource_data_to_file(url: str, resource: str, filepath: str):
    """Write 'link' or 'source' tags contents into file.

    Parameters:
        url: website url,
        resource: resource link,
        filepath: path to file.
    """
    resource_parse = urlparse(resource)
    if resource_parse.netloc:
        webpage_data = urlproc.get_webpage_contents(resource)
        write_to_file(filepath, webpage_data)
    else:
        webpage_data = requests.get(url + resource).content
        with open(filepath, 'wb+') as file_:
            file_.write(webpage_data)
