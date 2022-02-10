"Download a webpage into a folder."

import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path


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


def download_images(image_links, directory_path, url):
    """Download images from a website.

    Parameters:
        image_links: list of image sources,
        directory_path: path to the dir where the image will be stored.

    Returns:
        list of relative pathes to images.
    """
    list_of_img_relative_pathes = []
    for link in image_links:  # link = '/assets/professions/nodejs.png'
        r = requests.get(url + link).content
#        image_name = link[::-1].split('/')[0][::-1]  # nodejs.png

        src = link[:-len(Path(link).suffix)]
        # src = '/assets/professions/nodejs'
        link_name = ''.join([
            '-' if not i.isalpha() and not i.isdigit() else i for i in src
        ])  # -assets-professions-nodejs
        image_name = get_name(url) + link_name + Path(link).suffix

        path_to_image = os.path.join(directory_path, image_name)
        with open(path_to_image, 'wb+') as img:
            img.write(r)

        relative_path_to_image = (
            f'{get_directory_name(get_name(url))}/{image_name}'
        )
        list_of_img_relative_pathes.append(relative_path_to_image)

    return list_of_img_relative_pathes


def download(url, directory_path='current'):
    """Get path to file with a saved webpage.

    Parameters:
        dir_path: path to a directory with downloaded webpage,
        url: url of a webpage to be downloaded.
    """
    webpage_content = get_webpage_contents(url)
    filename = get_file_name(get_name(url))
    directoryname = get_directory_name(get_name(url))
    if directory_path == 'current':
        current = os.getcwd()
        directory_path = os.path.join(current, directoryname)
    else:
        directory_path = os.path.join(directory_path, directoryname)
    os.mkdir(directory_path)  # path/to/webpage-url_files
    # filepath for future HTML file
    filepath = os.path.join(directory_path, filename)

    file_contents = BeautifulSoup(webpage_content, 'html.parser')
    images = file_contents.find_all('img')  # find all the images
    list_of_images = []
    for link in images:
        list_of_images.append(link.get('src'))  # get image sources
    # download all the images from the file AND return list of pathes to images:
    list_of_image_relative_pathes = download_images(
        list_of_images,
        directory_path,
        url,
    )
    hash_table = dict(zip(list_of_images, list_of_image_relative_pathes))
    for link in images:
        link['src'] = hash_table[link['src']]

    write_to_file(filepath, file_contents.prettify())  # creating HTML file

    return filepath
