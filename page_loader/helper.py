"Helper functions for page_loader.py."

import logging
import os
import requests
import page_loader.io_functions as functions
from pathlib import Path
from progress.bar import IncrementalBar
from urllib.parse import urlparse


TAG_ATTRIBUTE_DICT = {'img': 'src', 'link': 'href', 'script': 'src'}


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


def get_directory_name(name):
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


def get_sources(tag, soup, webpage_url):
    """Get source info.

    Parameters:
        tag: 'img', 'link' or 'script',
        soup: bs4-ed webpage contents,
        website_url: website url.

    Returns:
        sources from bs4 and sources of image pathes.
    """
    list_of_sources = []
    sources = soup.find_all(tag)
    for source in sources:
        attribute = source.get(TAG_ATTRIBUTE_DICT[tag])
        if is_local(attribute, webpage_url):
            if tag == 'script':
                print(f'sources = {sources}\n')
                print(f'source = {source}')
                if source['src']:
                    list_of_sources.append(attribute)
            list_of_sources.append(attribute)
    return sources, list_of_sources


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
        url_core = prepare_url(url)
        logging.debug(f'Downloading {url_core + source}')
        filename = get_source_name(url_core, source)
        bar_ = IncrementalBar(f'{filename}', max=1, suffix='%(percent)d%%')
        filepath = os.path.join(path_to_directory, filename)
        try:
            functions.write_source_content_to_file(url_core, source, filepath)
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
            f'{get_directory_name(get_name(url))}/{filename}'
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
        source_name = get_website_name(url) + name + suffix
    return source_name


def process_source(tag, path_to_files, soup, url):
    """
    Process a source.

    Parameters:
        tag: tag: "img", "link", "script",
        path_to_files: path to a directory with downloaded files,
        soup: bs4-ed webpage contents,
        url: webpage url.
    """
    sources, list_of_sources = get_sources(tag, soup, url)
    logging.debug(f'Sources {tag} are being downloaded...')
    list_of_image_relative_pathes = download_source(
        url,
        path_to_files,
        list_of_sources,
    )
    logging.info(f'Sources {tag} successfully downloaded.')
    functions.replace_pathes(
        tag,
        sources,
        list_of_sources,
        list_of_image_relative_pathes,
    )
