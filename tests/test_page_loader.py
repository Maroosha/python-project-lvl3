from urllib.parse import urljoin
from page_loader.page_loader import download
from page_loader.namer import get_html_file_name
from page_loader.namer import get_directory_name
from page_loader.url_processor import get_webpage_contents
from page_loader.io_functions import write_to_file
import requests
import pytest
import os


URL = 'https://ru.hexlet.io/courses'

DIRECTORY_NAME = 'ru-hexlet-io-courses_files'
WEBPAGE_SOURCE = 'tests/fixtures/mocks/webpage_source.html'
DOWNLOADED_WEBSITE = 'tests/fixtures/downloaded_website.html'
CSS_URL = 'https://ru.hexlet.io/assets/application.css'
JS_URL = 'https://ru.hexlet.io/packs/js/runtime.js'
IMAGE_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
HTML_FIXTURE = 'ru-hexlet-io-courses.html'
INNER_HTML_FIXTURE = 'tests/fixtures/mocks/sub_html.html'
CSS_FIXTURE = 'tests/fixtures/mocks/css_file.css'
JS_FIXTURE = 'tests/fixtures/mocks/js_file.js'
IMAGE_FIXTURE = 'tests/fixtures/mocks/nodejs.png'
IMAGE = 'ru-hexlet-io-assets-professions-nodejs.png'
JS = 'ru-hexlet-io-packs-js-runtime.js'
CSS = 'ru-hexlet-io-assets-application.css'
INNER_HTML = 'ru-hexlet-io-courses.html'
INNER_HTML_PATH = 'ru-hexlet-io-courses_files/ru-hexlet-io-courses.html'
IMAGE_PATH = \
    'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
JS_PATH = 'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js'
CSS_PATH = 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css'
CODES = [403, 404, 500]
ERRORS = [
    requests.exceptions.HTTPError,
    requests.exceptions.Timeout,
]
downloaded_files = [
    (HTML_FIXTURE, DOWNLOADED_WEBSITE),
    (JS_PATH, JS_FIXTURE),
    (CSS_PATH, CSS_FIXTURE),
    (INNER_HTML_PATH, INNER_HTML_FIXTURE)
]


def read_file(filepath: str, flag='r'):
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
    correct_answer = DIRECTORY_NAME
    received_filepath = get_directory_name(URL)
    assert received_filepath == correct_answer


def test_get_file_name():
    "Test get_html_file_name function in page_loader module"
    correct_answer = HTML_FIXTURE
    received_filepath = get_html_file_name(URL)
    assert received_filepath == correct_answer


def test_write_to_file(tmp_path, requests_mock):
    "Test write_to_file function in page_loader module"
    correct_answer = read_file(WEBPAGE_SOURCE)
    requests_mock.get(URL, text=read_file(WEBPAGE_SOURCE))
    webpage_content = get_webpage_contents(URL)
    filepath = os.path.join(tmp_path, HTML_FIXTURE)
    write_to_file(filepath, webpage_content)
    received = read_file(filepath)
    assert received == correct_answer


@pytest.mark.parametrize('received, expected', downloaded_files)
def test_download(received, expected, tmp_path, requests_mock):
    'Test download() funcion.'
    requests_mock.get(URL, text=read_file(WEBPAGE_SOURCE))
    requests_mock.get(CSS_URL, text=read_file(CSS_FIXTURE))
    requests_mock.get(JS_URL, text=read_file(JS_FIXTURE))
    requests_mock.get(IMAGE_URL, content=read_file(IMAGE_FIXTURE, 'rb'))
    requests_mock.get(URL, text=read_file(INNER_HTML_FIXTURE))
    download(URL, tmp_path)
    received_file = os.path.join(tmp_path, received)
    received_png = os.path.join(tmp_path, IMAGE_PATH)
    assert read_file(received_file) == read_file(expected)
    assert read_file(received_png, 'rb') == read_file(IMAGE_FIXTURE, 'rb')


def test_for_permission_error(requests_mock):
    'Test for permission error.'
    requests_mock.get(URL, text=read_file(WEBPAGE_SOURCE))
    webpage_content = get_webpage_contents(URL)
    filepath = '/some_filepath'
    with pytest.raises(PermissionError):
        write_to_file(filepath, webpage_content)


@pytest.mark.parametrize('error', ERRORS)
def test_for_http_error(error, requests_mock, tmp_path):
    "Test for errors."
    requests_mock.get(URL, exc=error)
    with pytest.raises(error):
        assert not download(URL, tmp_path)


@pytest.mark.parametrize('code', CODES)
def test_repsonse_with_error(requests_mock, code, tmp_path):
    "Test for 403, 404 and 500 status codes."
    url = urljoin(URL, str(code))
    requests_mock.get(url, status_code=code)
    with pytest.raises(Exception):
        assert download(url, tmp_path)
