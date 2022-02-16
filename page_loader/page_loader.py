"Download a webpage into a folder."

import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse


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
    with open(filepath, 'w') as file_:
        file_.write(webpage_content)


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
        list_of_images: list of image sources

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
    "DOCSTR"
    list_of_links_relative_pathes = []
    for link in list_of_links:
        link_parse = urlparse(link)

        if Path(link).suffix: # link = '/assets/professions/nodejs.png'
            src = link[:-len(Path(link).suffix)]
            suffix = Path(link).suffix
        else:
            src = link # src = '/assets/professions/nodejs'
            suffix = '.html'
        if link_parse.scheme:
            src = src[len(link_parse.scheme) + 3:]
            source_name = ''.join([
                '-' if not i.isalpha() and not i.isdigit() else i for i in src
            ])  # -assets-professions-nodejs
            filename = source_name + suffix
        else:
            source_name = ''.join([
                '-' if not i.isalpha() and not i.isdigit() else i for i in src
            ])  # -assets-professions-nodejs
            filename = get_name(url) + source_name + suffix
        filepath = os.path.join(path_to_directory, filename)

        if link_parse.netloc:
            webpage_content = get_webpage_contents(link)
            write_to_file(filepath, webpage_content)
        else:
            webpage_content = requests.get(url + link).content
            with open(filepath, 'wb+') as file_:
                file_.write(webpage_content)

        relative_path_to_link = (
            f'{get_directory_name(get_name(url))}/{filename}'
        )
        list_of_links_relative_pathes.append(relative_path_to_link)
    return list_of_links_relative_pathes


def download_script(url, path_to_directory, list_of_scripts):
    "DOCSTR"
    list_of_scripts_relative_pathes = []

    for script_src in list_of_scripts:
        script_src_parse = urlparse(script_src)

#        if Path(script_src).suffix: # link = '/assets/professions/nodejs.png'
#            src = script_src[:-len(Path(script_src).suffix)]
#            suffix = Path(script_src).suffix
#        else:
#            src = script_src # src = '/assets/professions/nodejs'
#            suffix = '.html'
#        source_name = ''.join([
#            '-' if not i.isalpha() and not i.isdigit() else i for i in src
#        ])  # -assets-professions-nodejs
#        filename = get_name(url) + source_name + suffix
#        filepath = os.path.join(path_to_directory, filename)

        if Path(script_src).suffix: # link = '/assets/professions/nodejs.png'
            src = script_src[:-len(Path(script_src).suffix)]
            suffix = Path(script_src).suffix
        else:
            src = script_src # src = '/assets/professions/nodejs'
            suffix = '.html'
        if script_src_parse.scheme:
            src = src[len(script_src_parse.scheme) + 3:]
            source_name = ''.join([
                '-' if not i.isalpha() and not i.isdigit() else i for i in src
            ])  # -assets-professions-nodejs
            filename = source_name + suffix
        else:
            source_name = ''.join([
                '-' if not i.isalpha() and not i.isdigit() else i for i in src
            ])  # -assets-professions-nodejs
            filename = get_name(url) + source_name + suffix
        filepath = os.path.join(path_to_directory, filename)

        if script_src_parse.netloc:
            webpage_content = get_webpage_contents(script_src)
            write_to_file(filepath, webpage_content)
        else:
            webpage_content = requests.get(url + script_src).content
            with open(filepath, 'wb+') as file_:
                file_.write(webpage_content)

        relative_path_to_link = (
            f'{get_directory_name(get_name(url))}/{filename}'
        )
        list_of_scripts_relative_pathes.append(relative_path_to_link)

    return list_of_scripts_relative_pathes


def download(url, directory_path='current'):
    """Get path to file with a saved webpage.

    Parameters:
        dir_path: path to a directory with downloaded webpage,
        url: url of a webpage to be downloaded.
    """
    webpage_content = get_webpage_contents(url)
    filename = get_file_name(get_name(url))
    if directory_path == 'current':
        directory_path = os.getcwd()
    # filepath for a future HTML file
    filepath = os.path.join(directory_path, filename)

    # create a dicrecotry for files
    directoryname_files = get_directory_name(get_name(url))
    directorypath_files = os.path.join(directory_path, directoryname_files)
    os.mkdir(directorypath_files)  # path/to/webpage-url_files

    file_contents = BeautifulSoup(webpage_content, 'html.parser')
    images = file_contents.find_all('img')  # find all the images
    list_of_images = []
    for source in images:
        list_of_images.append(source.get('src'))  # get image sources

    list_of_links = []
    links = file_contents.find_all('link')  # find all the links
    for link in links:
        href = link.get('href')
        if is_local(href):  # checking if it is local
            list_of_links.append(href)  # get links sources

    list_of_scripts = []
    scripts = file_contents.find_all('script')  # find all the scripts: with and without 'src'
    for script in scripts:
        src = script.get('src')
        if is_local(src) and script['src']:
            list_of_scripts.append(src)  # get scripts sources


    # download all the files AND return list of pathes to them:
    list_of_image_relative_pathes = download_image(url, directorypath_files,  list_of_images)
    list_of_links_relative_pathes = download_link(url, directorypath_files, list_of_links)
    list_of_scripts_relative_pathes = download_script(url, directorypath_files, list_of_scripts)

    images_hash_table = dict(zip(list_of_images, list_of_image_relative_pathes))
    for source in images:
        source['src'] = images_hash_table[source['src']]

    links_hash_table = dict(zip(list_of_links, list_of_links_relative_pathes))
    for link in links:
        href = link.get('href')
        if href in links_hash_table:
            link['href'] = links_hash_table[link['href']]

    scripts_hash_table = dict(zip(list_of_scripts, list_of_scripts_relative_pathes))
    for script in scripts:
        src = script.get('src')
        if src in scripts_hash_table:
            script['src'] = scripts_hash_table[script['src']]

    write_to_file(filepath, file_contents.prettify())  # creating an HTML file

    return filepath
