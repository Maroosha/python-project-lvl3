from page_loader.page_loader import download
from page_loader.functions import get_file_name
from page_loader.functions import get_directory_name, get_name
from page_loader.functions import get_webpage_contents
from page_loader.functions import write_to_file
import requests_mock
import tempfile
import os


def read_file(filepath, flag='r'):
    """Read a file.

    Parameters:
        filepath: path to file.

    Returns:
        data from file.
    """
    with open(filepath, flag) as file_:
        return file_.read()


def test_get_directory_name():
    "Test get_directory_name function in page_loader module"
    name = get_name('https://ru.hexlet.io')
    correct_answer = 'ru-hexlet-io_files'
    received_filepath = get_directory_name(name)
    assert received_filepath == correct_answer


def test_get_file_name():
    "Test get_file_name function in page_loader module"
    name = get_name('https://ru.hexlet.io')
    correct_answer = 'ru-hexlet-io.html'
    received_filepath = get_file_name(name)
    assert received_filepath == correct_answer


def test_write_to_file():
    "Test write_to_file function in page_loader module"
    with tempfile.TemporaryDirectory() as temporary_directory:
        correct_answer = read_file('tests/fixtures/mocks/webpage_source.html')
        with requests_mock.Mocker() as mock:
            mock.get(
                'https://ru.hexlet.io',
                text=read_file('tests/fixtures/mocks/webpage_source.html'),
            )
            webpage_content = get_webpage_contents('https://ru.hexlet.io')
            filepath = os.path.join(
                temporary_directory,
                'ru-hexlet-io.html',
            )
            write_to_file(filepath, webpage_content)
            received = read_file(filepath)
            assert received == correct_answer


def test_download():
    "Test download function in page_loader module"
    with tempfile.TemporaryDirectory() as temporary_directory:
        correct_answer = read_file('tests/fixtures/downloaded_website.html')
        with requests_mock.Mocker() as mock:
            mock.get(
                'https://ru.hexlet.io',
                text=read_file('tests/fixtures/mocks/webpage_source.html'),
            )  # mock file contents
            mock.get(
                'https://ru.hexlet.io/assets/application.css',
                text=read_file('tests/fixtures/mocks/css_file.css'),
            )
            mock.get(
                'https://ru.hexlet.io/packs/js/runtime.js',
                text=read_file('tests/fixtures/mocks/js_file.js'),
            )
            mock.get(
                'https://ru.hexlet.io/assets/professions/nodejs.png',
                content=read_file('tests/fixtures/mocks/nodejs.png', 'rb'),
            )
            mock.get(
                'https://ru.hexlet.io/courses',
                text=read_file('tests/fixtures/mocks/sub_html.html'),
            )

            download('https://ru.hexlet.io', temporary_directory)
            received = read_file(os.path.join(
                temporary_directory,
                'ru-hexlet-io.html',
            ))  # HTML file

            directorypath_files = os.path.join(
                temporary_directory,
                get_directory_name(get_name('https://ru.hexlet.io')),
            )  # folder for supporting files
            # check if 'ru-hexlet-io-courses_files' already exists
            if not os.path.isdir(directorypath_files):
                os.mkdir(directorypath_files)

            assert received == correct_answer
            assert os.path.isfile(
                    os.path.join(
                    directorypath_files,
                    'ru-hexlet-io-assets-professions-nodejs.png',
                )
            )
            assert os.path.isfile(
                    os.path.join(
                    directorypath_files,
                    'ru-hexlet-io-packs-js-runtime.js',
                )
            )
            assert os.path.isfile(
                    os.path.join(
                    directorypath_files,
                    'ru-hexlet-io-assets-application.css',
                )
            )
            assert os.path.isfile(
                    os.path.join(
                    directorypath_files,
                    'ru-hexlet-io-courses.html',
                )
            )
