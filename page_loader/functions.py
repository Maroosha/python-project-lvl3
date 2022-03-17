"Auxilary functions for page_loader.py."

import logging
import os
import requests
import page_loader.helper as helper
from pathlib import Path
from progress.bar import IncrementalBar
from urllib.parse import urlparse


TAG_ATTRIBUTE_DICT = {'img': 'src', 'link': 'href', 'script': 'src'}


def download_source(url, path_to_directory, list_of_sources):
    """Download resources from 'image', 'link', 'scripts' tag.

    Parameters:
        url: website url,
        path_to_directory: path to the dir where the source will be stored,
        list_of_links: list of links.

    Returns:
        list of relative pathes to links.
    """
    list_of_source_relative_pathes = []
    for source in list_of_sources:
        url_core = helper.prepare_url(url)
        logging.debug(f'Downloading {url_core + source}')
        filename = get_source_name(url_core, source)
        bar_ = IncrementalBar(f'{filename}', max=1, suffix='%(percent)d%%')
        filepath = os.path.join(path_to_directory, filename)
        try:
            write_source_content_to_file(url_core, source, filepath)
            bar_.next()
        except PermissionError as error1:
            print(f'Access denied to file {filepath}.')
            logging.error('Access denied to file %s.', filepath)
            raise error1
        except OSError as error2:
            print(f'Unable to save data to {filepath}.')
            logging.error('Unable to save data to %s.', filepath)
            raise error2
        logging.debug('Path_to_link: %s', filepath)
        relative_path_to_link = (
            f'{helper.get_directory_name(helper.get_name(url))}/{filename}'
        )
        bar_.next()
        list_of_source_relative_pathes.append(relative_path_to_link)
        bar_.finish()
    return list_of_source_relative_pathes


def get_source_name(url, source):
    """Get name of the link/script source (filename).

    Parameters:
        url: website url,
        source: source link.

    Returns:
        name of the source.
    """
    source_parse = urlparse(source)
    if Path(source).suffix:  # link = '/assets/professions/nodejs.png'
        src = source[:-len(Path(source).suffix)]
        suffix = Path(source).suffix
    else:
        src = source  # src = '/assets/professions/nodejs'
        suffix = '.html'
    if source_parse.scheme:
        src = src[len(source_parse.scheme) + 3:]
        name = ''.join([
            '-' if not i.isalpha() and not i.isdigit() else i for i in src
        ])  # -assets-professions-nodejs
        source_name = name + suffix
    else:
        name = ''.join([
            '-' if not i.isalpha() and not i.isdigit() else i for i in src
        ])  # -assets-professions-nodejs
        source_name = helper.get_website_name(url) + name + suffix
    return source_name


def write_source_content_to_file(url, source, filepath):
    """Write 'link' or 'source' tags contents into file.

    Parameters:
        url: website url,
        source: source link,
        filepath: path to file.
    """
    source_parse = urlparse(source)
    if source_parse.netloc:
        webpage_content = helper.get_webpage_contents(source)
        helper.write_to_file(filepath, webpage_content)
    else:
        webpage_content = requests.get(url + source).content
        with open(filepath, 'wb+') as file_:
            file_.write(webpage_content)


def get_sources(tag, file_contents, webpage_url):
    """Get source info.

    Parameters:
        tag: 'img', 'link' or 'script',
        file_contents: bs4-ed webpage contents,
        website_url: website url.

    Returns:
        images from bs4 and list of image pathes.
    """
    list_of_sources = []
    sources = file_contents.find_all(tag)
    for source in sources:
        attribute = source.get(TAG_ATTRIBUTE_DICT[tag])
        if helper.is_local(attribute, webpage_url):
            if tag == 'script' and source['src']:
                list_of_sources.append(attribute)
            list_of_sources.append(attribute)
    return sources, list_of_sources


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
