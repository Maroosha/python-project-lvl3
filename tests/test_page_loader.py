from page_loader.page_loader import download, get_file_name
from page_loader.page_loader import get_directory_name, get_name
from page_loader.page_loader import get_webpage_contents
from page_loader.page_loader import write_to_file
# import requests_mock
import tempfile
import os


def read_file(filepath):
    """Read a file.

    Parameters:
        filepath: path to file.

    Returns:
        data from file.
    """
    with open(filepath) as file_:
        return file_.read()


def tests_get_directory_name():
    "Test get_directory_name function in page_loader module"
    name = get_name('https://page-loader.hexlet.repl.co')
    correct_answer = 'page-loader-hexlet-repl-co_files'
    received_filepath = get_directory_name(name)
    assert received_filepath == correct_answer


def tests_get_file_name():
    "Test get_file_name function in page_loader module"
    name = get_name('https://page-loader.hexlet.repl.co')
    correct_answer = 'page-loader-hexlet-repl-co.html'
    received_filepath = get_file_name(name)
    assert received_filepath == correct_answer


def tests_write_to_file():
    "Test write_to_file function in page_loader module"
    with tempfile.TemporaryDirectory() as temporary_directory:
        directory_path = os.path.join(
            temporary_directory,
            get_directory_name(get_name('https://page-loader.hexlet.repl.co')),
        )
        os.mkdir(directory_path)
        correct_answer = read_file('tests/fixtures/original_website.html')
        webpage_content = get_webpage_contents('https://page-loader.hexlet.repl.co')
        filepath = os.path.join(
            temporary_directory,
            'page-loader-hexlet-repl-co_files/page-loader-hexlet-repl-co.html',
        )
        write_to_file(filepath, webpage_content)
        received = read_file(filepath)
        assert received == correct_answer


def tests_download():
    "Test download function in page_loader module"
    with tempfile.TemporaryDirectory() as temporary_directory:
        correct_answer = read_file('tests/fixtures/downloaded_website.html')
        download('https://page-loader.hexlet.repl.co', temporary_directory)
        directory_path = os.path.join(
            temporary_directory,
            get_directory_name(get_name('https://page-loader.hexlet.repl.co')),
        )
        # check if 'page-loader-hexlet-repl-co_files' already exists
        if not os.path.isdir(directory_path):
            os.mkdir(directory_path)
        received = read_file(os.path.join(
            directory_path,
            'page-loader-hexlet-repl-co.html',
        ))
        assert received == correct_answer
        assert os.path.isfile(
            os.path.join(
                directory_path,
                'page-loader-hexlet-repl-co-assets-professions-nodejs.png',
            )
        )