"Download a webpage into a folder."

import logging
import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse


class KnownError(Exception):
    "Some known error."
    pass


def get_name(url):
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


def get_file_name(name):
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
    request = requests.get(url)
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
    except OSError:
        logging.error('Unable to write to file %s.', filepath)


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
        r = requests.get(url + source).content
        src = source[:-len(Path(source).suffix)]
        # src = '/assets/professions/nodejs'
        source_name = ''.join([
            '-' if not i.isalpha() and not i.isdigit() else i for i in src
        ])  # -assets-professions-nodejs
        image_name = get_name(url) + source_name + Path(source).suffix
        path_to_image = os.path.join(path_to_directory, image_name)
        with open(path_to_image, 'wb+') as img:
            img.write(r)
        relative_path_to_image = (
            f'{get_directory_name(get_name(url))}/{image_name}'
        )
        list_of_image_relative_pathes.append(relative_path_to_image)
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
        filename = get_source_name(url, link)
        filepath = os.path.join(path_to_directory, filename)
        write_source_content_to_file(url, link, filepath)
        relative_path_to_link = (
            f'{get_directory_name(get_name(url))}/{filename}'
        )
        list_of_links_relative_pathes.append(relative_path_to_link)
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
        filepath = os.path.join(path_to_directory, filename)
        write_source_content_to_file(url, script_src, filepath)
        relative_path_to_link = (
            f'{get_directory_name(get_name(url))}/{filename}'
        )
        list_of_scripts_relative_pathes.append(relative_path_to_link)
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
        source_name = get_name(url) + name + suffix
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
    images = file_contents.find_all('img')
    list_of_images = []
    for image in images:
        list_of_images.append(image.get('src'))
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
    for link in links:
        href = link.get('href')
        if is_local(href):
            list_of_links.append(href)
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
    for script in scripts:
        src = script.get('src')
        if is_local(src) and script['src']:
            list_of_scripts.append(src)
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


def download(url, directory_path='current'):
    """Get path to file with a saved webpage.

    Parameters:
        dir_path: path to a directory with downloaded webpage,
        url: url of a webpage to be downloaded.
    """
    webpage_content = get_webpage_contents(url)
    logging.debug('Webpage contents retrieved.')
    filename = get_file_name(get_name(url))
    if directory_path == 'current':
        directory_path = os.getcwd()
    filepath = os.path.join(directory_path, filename)
    logging.info('Webpage contents will be stored in %s.', filepath)

    # create a dicrecotry for files
    directoryname_files = get_directory_name(get_name(url))
    directorypath_files = os.path.join(directory_path, directoryname_files)
    try:
        os.mkdir(directorypath_files)  # path/to/webpage-url_files
    except OSError:
        logging.exception('Unable to create directory %s.', directorypath_files)
    logging.info('Downloaded files will be stored in %s.', directorypath_files)

    # parse webpage contents
    file_contents = BeautifulSoup(webpage_content, 'html.parser')
    logging.debug('Webpage contents is being parsed...')
    images, list_of_images = get_images(file_contents)
    links, list_of_links = get_links(file_contents)
    scripts, list_of_scripts = get_scripts(file_contents)

    # download all the files and return list of pathes to them:
    logging.debug('Images are being downloaded...')
    list_of_image_relative_pathes = download_image(
        url,
        directorypath_files,
        list_of_images,
    )
    logging.info('Images successfully downloaded.')
    logging.debug('Sources are being downloaded...')  # links???
    list_of_links_relative_pathes = download_link(
        url,
        directorypath_files,
        list_of_links,
    )
    logging.info('Sources successfully downloaded.')  # or links???
    logging.debug('Scripts are being downloaded...')
    list_of_scripts_relative_pathes = download_script(
        url,
        directorypath_files,
        list_of_scripts,
    )
    logging.info('Scripts successfully downloaded.')

    # replace relative pathes (imgs, links, scripts[src]) in webpage contents
    replace_image_pathes(images, list_of_images, list_of_image_relative_pathes)
    replace_pathes(links, list_of_links, list_of_links_relative_pathes, 'href')
    replace_pathes(
        scripts, list_of_scripts, list_of_scripts_relative_pathes, 'src',
    )

    write_to_file(filepath, file_contents.prettify())
    logging.info('Webpage contents successfully saved in %s.', filepath)

    print(f'Webpage contents successfully saved in \
{filepath} and {directorypath_files}.')
    return filepath
