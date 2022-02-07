from page_loader.page_loader import download
from page_loader.page_loader import get_webpage_content
from page_loader.page_loader import write_to_file
import requests_mock
import tempfile
import os


def read_file(filepath):
    """Read a file.

    Parameters:
        filepath; path to file.

    Returns:
        data from file.
    """
    with open(filepath) as file_:
        return file_.read()


def tests_page_loader_write_to_file():
    "Test download function in page_loader module"
    with tempfile.TemporaryDirectory() as temporary_directory:
        correct_answer = read_file('tests/fixtures/downloaded_website.html')
        webpage_content = get_webpage_content('https://page-loader.hexlet.repl.co')
        filepath = os.path.join(temporary_directory, 'page-loader-hexlet-repl-co.html')
        write_to_file(filepath, webpage_content)
        received = read_file(filepath)
        assert received == correct_answer



def tests_page_loader_get_file_name():
    "Test get_file_name function in page_loader module"
    with tempfile.TemporaryDirectory() as temporary_directory:
        correct_answer = os.path.join(temporary_directory, 'page-loader-hexlet-repl-co.html')
        received_filepath = download(
            'https://page-loader.hexlet.repl.co',
            temporary_directory,
        )
        assert received_filepath == correct_answer


def tests_page_loader_download():
    "Test download function in page_loader module"
    with tempfile.TemporaryDirectory() as temporary_directory:
        with requests_mock.Mocker() as mock_:
            correct_answer = read_file('tests/fixtures/downloaded_website.html')
            # instead of requests
            mock_.get('https://page-loader.hexlet.repl.co', text=correct_answer)
            download('https://page-loader.hexlet.repl.co', temporary_directory)
            # => page-loader-hexlet-repl-co.html inside temporary dir
            received = read_file(os.path.join(
                temporary_directory,
                'page-loader-hexlet-repl-co.html',
            ))
            assert received == correct_answer
