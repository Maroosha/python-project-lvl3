from urllib.parse import urljoin
from page_loader.page_loader import download
from page_loader.functions import get_main_file_name
from page_loader.functions import get_directory_name, get_name
from page_loader.functions import get_webpage_contents
from page_loader.functions import write_to_file
import logging
import requests_mock
import requests
import pytest
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
    name = get_name('https://ru.hexlet.io/courses')
    correct_answer = 'ru-hexlet-io-courses_files'
    received_filepath = get_directory_name(name)
    assert received_filepath == correct_answer


def test_get_file_name():
    "Test get_main_file_name function in page_loader module"
    name = get_name('https://ru.hexlet.io/courses')
    correct_answer = 'ru-hexlet-io-courses.html'
    received_filepath = get_main_file_name(name)
    assert received_filepath == correct_answer


def test_write_to_file():
    "Test write_to_file function in page_loader module"
    with tempfile.TemporaryDirectory() as temporary_directory:
        correct_answer = read_file('tests/fixtures/mocks/webpage_source.html')
        with requests_mock.Mocker() as mock:
            mock.get(
                'https://ru.hexlet.io/courses',
                text=read_file('tests/fixtures/mocks/webpage_source.html'),
            )
            webpage_content = get_webpage_contents(
                'https://ru.hexlet.io/courses',
            )
            filepath = os.path.join(
                temporary_directory,
                'ru-hexlet-io-courses.html',
            )
            write_to_file(filepath, webpage_content)
            received = read_file(filepath)
            assert received == correct_answer


def test_download():
    "Test download function in page_loader module"
    logging.debug('Test start')
    with tempfile.TemporaryDirectory() as temporary_directory:
        correct_answer = read_file('tests/fixtures/downloaded_website.html')
        with requests_mock.Mocker() as mock:
            mock.get(
                'https://ru.hexlet.io/courses',
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

            filepath = download(
                'https://ru.hexlet.io/courses',
                temporary_directory,
            )
            received = read_file(os.path.join(
                temporary_directory,
                'ru-hexlet-io-courses.html',
            ))  # HTML file

            directorypath_files = os.path.join(
                temporary_directory,
                get_directory_name(get_name('https://ru.hexlet.io/courses')),
            )
            if not os.path.isdir(directorypath_files):
                os.mkdir(directorypath_files)

            assert os.path.exists(filepath)
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


def test_for_http_errors():
    "Test for HTTP errors."
    with tempfile.TemporaryDirectory() as temporary_directory:
        with requests_mock.Mocker() as mock:
            # Note to self:
            # register_uri() takes the HTTP method, the URI and then information
            # that is used to build the response.
            mock.register_uri(
                'GET',
                'https://ru.hexlet.io/courses',
                exc=requests.HTTPError,
            )
            # exc=exception that will be raised instead of returning a response.
            # see https://requests-mock.readthedocs.io/en/latest/response.html
            # see +
            # https://stackoverflow.com/questions/19342111/get-http-error-code-from-requests-exceptions-httperror
            with pytest.raises(requests.HTTPError) as exc_info:
                download('https://ru.hexlet.io/courses', temporary_directory)
            assert exc_info.type is requests.HTTPError


@pytest.mark.parametrize('code', [403, 404, 500])
def test_repsonse_with_error(requests_mock, code):
    "Test for 404 and 500 status codes."
    url = urljoin('https://ru.hexlet.io/courses', str(code))
    requests_mock.get(url, status_code=code)
    with tempfile.TemporaryDirectory() as temporary_directory:
        with pytest.raises(Exception):
            assert download(url, temporary_directory)
