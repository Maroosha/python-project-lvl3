"Download a webpage into a folder."

import os
import requests


def get_file_name(url):
    """Get a name of a file containing downloaded webpage.

    Parameters:
        url: webpage url.

    Returns:
        name of a file containing the downloaded webpage.
    """
    address = url.split('//')[1]
    filename = ['-' if i.isalpha() or i.isdigit() else i for i in address]
    return ''.join(filename) + '.html'


def get_webpage_content(url):
    """Request data from a webpage.

    Parameters:
        url: webpage url.

    Returns:
        webpage content.
    """
    request = requests.get(url)
    return request.text


def write_to_file(filename, webpage_content):
    """Write webpage content to file.

    Parameters:
        url: webpage url,
        filename: filename to store webpage content.
    """
    with open(filename, 'w') as file_:
        file_.write(webpage_content)


def download(url, directory_path='current'):
    """Get path to file with a saved webpage.

    Parameters:
        dir_path: path to a directory with downloaded webpage,
        url: url of a webpage to be downloaded.

    Returns:
        path to file with a saved webpage
    """
    webpage_content = get_webpage_content(url)
    filename = get_file_name(url)
    write_to_file(filename, webpage_content)
    if directory_path == 'current':
        directory_path = os.getcwd()
    return os.path.join(directory_path, filename)
