"Auxilary functions for page_loader.py."

import logging
import os
import requests
from pathlib import Path
from progress.bar import IncrementalBar
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


def is_local(url):
    """Check whether a resource is local or not
    (if it belongs to ru.hexlet.io).

    Parameters:
        url: url from src/href.

    Returns:
        true if local, false if not
    """
    parse_result = urlparse(str(url))
    return parse_result.netloc == 'ru.hexlet.io' or parse_result.netloc == ''


def download_image(url, path_to_directory, list_of_images):
    """Download images from a website.

    Parameters:
        url: website url,
        path_to_directory: path to the dir where the image will be stored,
        list_of_images: list of images.

    Returns:
        list of relative pathes to images.
    """
    list_of_image_relative_pathes = []
    for source in list_of_images:  # source = '/assets/professions/nodejs.png'
        logging.debug(f'Downloading {url}, {source}')
        r = requests.get(url + source).content
        src = source[:-len(Path(source).suffix)]
        # src = '/assets/professions/nodejs'
        source_name = ''.join([
            '-' if not i.isalpha() and not i.isdigit() else i for i in src
        ])  # -assets-professions-nodejs
        image_name =  get_website_name(url) + source_name + Path(source).suffix
        logging.debug(f'image name: {image_name}')
        bar_ = IncrementalBar(f'{image_name}', max=1, suffix='%(percent)d%%')
        path_to_image = os.path.join(path_to_directory, image_name)
        try:
            with open(path_to_image, 'wb+') as img:
                img.write(r)
                bar_.next()
        except PermissionError as error1:
            print(f'Access denied to file {path_to_image}.')
            logging.error('Access denied to file %s.', path_to_image)
            raise error1
        except OSError as error2:
            print(f'Unable to save data to {path_to_image}.')
            logging.error('Unable to save an image as %s.', path_to_image)
            raise error2
        logging.debug('Path_to_image: %s', path_to_image)
        relative_path_to_image = (
            f'{get_directory_name(get_name(url))}/{image_name}'
        )
        bar_.next()
        list_of_image_relative_pathes.append(relative_path_to_image)
        bar_.finish()
    return list_of_image_relative_pathes


def download_link(url, path_to_directory, list_of_links):
    """Download resources from 'link' tag.

    Parameters:
        url: website url,
        path_to_directory: path to the dir where the image will be stored,
        list_of_links: list of links.

    Returns:
        list of relative pathes to links.
    """
    list_of_links_relative_pathes = []
    for link in list_of_links:
        logging.debug(f'Downloading {url + link}')
        filename = get_source_name(url, link)
        bar_ = IncrementalBar(f'{filename}', max=1, suffix='%(percent)d%%')
        filepath = os.path.join(path_to_directory, filename)
        try:
            write_source_content_to_file(url, link, filepath)
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
        list_of_links_relative_pathes.append(relative_path_to_link)
        bar_.finish()
    return list_of_links_relative_pathes


def download_script(url, path_to_directory, list_of_scripts):
    """Download resources from 'script' tag if there is 'src' attribute.

    Parameters:
        url: website url,
        path_to_directory: path to the dir where the image will be stored,
        list_of_images: list of scripts.

    Returns:
        list of relative pathes to scripts.
    """
    list_of_scripts_relative_pathes = []
    for script_src in list_of_scripts:
        filename = get_source_name(url, script_src)
        bar_ = IncrementalBar(f'{filename}', max=1, suffix='%(percent)d%%')
        filepath = os.path.join(path_to_directory, filename)
        try:
            write_source_content_to_file(url, script_src, filepath)
            bar_.next()
        except PermissionError as error1:
            print(f'Access denied to file {filepath}.')
            logging.error('Access denied to file %s.', filepath)
            raise error1
        except OSError as error2:
            print(f'Unable to save data to {filepath}.')
            logging.error('Unable to save data to %s.', filepath)
            raise error2
        relative_path_to_link = (
            f'{get_directory_name(get_name(url))}/{filename}'
        )
        bar_.next()
        list_of_scripts_relative_pathes.append(relative_path_to_link)
        bar_.finish()
    return list_of_scripts_relative_pathes


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


def write_source_content_to_file(url, source, filepath):
    """Write 'link' or 'source' tags contents into file.

    Parameters:
        url: website url,
        source: source link,
        filepath: path to file.
    """
    source_parse = urlparse(source)
    if source_parse.netloc:
        webpage_content = get_webpage_contents(source)
        write_to_file(filepath, webpage_content)
    else:
        webpage_content = requests.get(url + source).content
        with open(filepath, 'wb+') as file_:
            file_.write(webpage_content)


def get_images(file_contents):
    """Get images info.

    Parameters:
        file_contents: bs4-ed webpage contents.

    Returns:
        images from bs4 and list of image pathes.
    """
    list_of_images = []
    images = file_contents.find_all('img')
    logging.debug(f'file_contents.find_all("img"): \
{file_contents.find_all("img")}')
    for image in images:
        list_of_images.append(image.get('src'))
        logging.debug(F'image: {image.get("src")}')
    logging.debug('list of images: %s', list_of_images)
    return images, list_of_images


def get_links(file_contents):
    """Get links info.

    Parameters:
        file_contents: bs4-ed webpage contents.

    Returns:
        links from bs4 and list of links pathes.
    """
    list_of_links = []
    links = file_contents.find_all('link')
    logging.debug(f'file_contents.find_all("link"): \
{file_contents.find_all("link")}')
    for link in links:
        href = link.get('href')
        if is_local(href):
            list_of_links.append(href)
            logging.debug(F'link: {link.get("link")}')
    logging.debug('list of links: %s', list_of_links)
    return links, list_of_links


def get_scripts(file_contents):
    """Get scripts info.

    Parameters:
        file_contents: bs4-ed webpage contents.

    Returns:
        scripts from bs4 and list of scripts pathes.
    """
    list_of_scripts = []
    scripts = file_contents.find_all('script')
    logging.debug(f'file_contents.find_all("script"): \
{file_contents.find_all("script")}')
    for script in scripts:
        src = script.get('src')
        if is_local(src) and script['src']:
            list_of_scripts.append(src)
            logging.debug(F'sript: {src}')
    logging.debug('list of scripts: %s', list_of_scripts)
    return scripts, list_of_scripts


def replace_image_pathes(images, list_of_images, relative_pathes):
    """Replace image pathes with their relative pathes.

    Parameters:
        images: bs4-ed images,
        list_of_images: path to an image,
        relative_pathes: relative pathe to an image.
    """
    hash_table = dict(zip(list_of_images, relative_pathes))
    for source in images:
        source['src'] = hash_table[source['src']]


def replace_pathes(sources, list_of_sources, relative_pathes, attribute):
    """Replace links/sources pathes with their relative pathes.

    Parameters:
        source: bs4-ed links/sources,
        list_of_images: path to a link/source,
        relative_pathes: relative pathe to a link/source.
    """
    hash_table = dict(zip(list_of_sources, relative_pathes))
    for source in sources:
        attr = source.get(attribute)
        if attr in hash_table:
            source[attribute] = hash_table[source[attribute]]
