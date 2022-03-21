"Auxilary functions for page_loader.py."

import logging
import requests
import page_loader.helper as helper
from urllib.parse import urlparse


TAG_ATTRIBUTE_DICT = {'img': 'src', 'link': 'href', 'script': 'src'}


def write_to_file(filepath, data):
    """Write webpage content to file.

    Parameters:
        url: webpage url,
        filepath: path to file.
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


def write_source_content_to_file(url, source, filepath):
    """Write 'link' or 'source' tags contents into file.

    Parameters:
        url: website url,
        source: source link,
        filepath: path to file.
    """
    source_parse = urlparse(source)
    if source_parse.netloc:
        webpage_data = helper.get_webpage_contents(source)
        write_to_file(filepath, webpage_data)
    else:
        webpage_data = requests.get(url + source).content
        with open(filepath, 'wb+') as file_:
            file_.write(webpage_data)


def replace_pathes(tag, sources, list_of_sources, relative_pathes):
    """Replace pathes to sources with their relative pathes.

    Parameters:
        tag: 'img', 'link' or 'script',
        source: bs4-ed links/sources,
        list_of_images: path to a link/source,
        relative_pathes: relative path to a link/source.
    """
    hash_table = dict(zip(list_of_sources, relative_pathes))
    for source in sources:
        attr = source.get(TAG_ATTRIBUTE_DICT[tag])
        if attr in hash_table:
            source[TAG_ATTRIBUTE_DICT[tag]] = \
                hash_table[source[TAG_ATTRIBUTE_DICT[tag]]]
