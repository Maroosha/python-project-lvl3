from urllib.parse import urljoin
from page_loader.page_loader import download
from page_loader.helper import get_main_file_name
from page_loader.helper import get_directory_name, get_name
from page_loader.helper import get_webpage_contents
from page_loader.helper import write_to_file
import requests
import pytest
import os


CODES = [403, 404, 500]
ERRORS = [
    requests.exceptions.HTTPError,
    requests.exceptions.Timeout,
    PermissionError,
]
URL = 'https://ru.hexlet.io/courses'
DIRECTORY_NAME = 'ru-hexlet-io-courses_files'
HTML_FILE = 'ru-hexlet-io-courses.html'
INNER_HTML_FILE = 'tests/fixtures/mocks/sub_html.html'
WEBPAGE_SOURCE = 'tests/fixtures/mocks/webpage_source.html'
DOWNLOADED_WEBSITE = 'tests/fixtures/downloaded_website.html'
CSS_URL = 'https://ru.hexlet.io/assets/application.css'
JS_URL = 'https://ru.hexlet.io/packs/js/runtime.js'
IMAGE_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
CSS_FILE = 'tests/fixtures/mocks/css_file.css'
JS_FILE = 'tests/fixtures/mocks/js_file.js'
IMAGE = 'tests/fixtures/mocks/nodejs.png'
IMAGE_PATH = 'ru-hexlet-io-assets-professions-nodejs.png'
JS_PATH = 'ru-hexlet-io-packs-js-runtime.js'
CSS_PATH = 'ru-hexlet-io-assets-application.css'
INNER_HTML_PATH = 'ru-hexlet-io-courses.html'


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
    name = get_name(URL)
    correct_answer = DIRECTORY_NAME
    received_filepath = get_directory_name(name)
    assert received_filepath == correct_answer


def test_get_file_name():
    "Test get_main_file_name function in page_loader module"
    name = get_name(URL)
    correct_answer = HTML_FILE
    received_filepath = get_main_file_name(name)
    assert received_filepath == correct_answer


def test_write_to_file(tmp_path, requests_mock):
    "Test write_to_file function in page_loader module"
    correct_answer = read_file(WEBPAGE_SOURCE)
    requests_mock.get(URL, text=read_file(WEBPAGE_SOURCE))
    webpage_content = get_webpage_contents(URL)
    filepath = os.path.join(tmp_path, HTML_FILE)
    write_to_file(filepath, webpage_content)
    received = read_file(filepath)
    assert received == correct_answer


def test_download(tmp_path, requests_mock):
    "Test download function in page_loader module"
    correct_answer = read_file(DOWNLOADED_WEBSITE)
    requests_mock.get(URL, text=read_file(WEBPAGE_SOURCE))
    requests_mock.get(CSS_URL, text=read_file(CSS_FILE))
    requests_mock.get(JS_URL, text=read_file(JS_FILE))
    requests_mock.get(IMAGE_URL, content=read_file(IMAGE, 'rb'))
    requests_mock.get(URL, text=read_file(INNER_HTML_FILE))

    filepath = download(URL, tmp_path)
    received = read_file(os.path.join(tmp_path, HTML_FILE))

    directorypath_files = os.path.join(tmp_path, DIRECTORY_NAME)

    assert os.path.exists(filepath)
    assert received == correct_answer
    assert os.path.isfile(
        os.path.join(directorypath_files, IMAGE_PATH),
    )
    assert read_file(
        os.path.join(directorypath_files, IMAGE_PATH),
        'rb',
    ) == read_file(IMAGE, 'rb')
    assert os.path.isfile(
        os.path.join(directorypath_files, JS_PATH),
    )
    assert read_file(
        os.path.join(directorypath_files, JS_PATH),
    ) == read_file(JS_FILE)
    assert os.path.isfile(
        os.path.join(directorypath_files, CSS_PATH),
    )
    assert read_file(
        os.path.join(directorypath_files, CSS_PATH),
    ) == read_file(CSS_FILE)
    assert os.path.isfile(
        os.path.join(directorypath_files, INNER_HTML_PATH),
    )
    assert read_file(
        os.path.join(directorypath_files, INNER_HTML_PATH),
    ) == read_file(INNER_HTML_FILE)


@pytest.mark.parametrize('error', ERRORS)
def test_for_http_error(error, requests_mock, tmp_path):
    "Test for errors."
    requests_mock.get(URL, exc=error)
    with pytest.raises(error):
        download(URL, tmp_path)


@pytest.mark.parametrize('code', CODES)
def test_repsonse_with_error(requests_mock, code, tmp_path):
    "Test for 403, 404 and 500 status codes."
    url = urljoin(URL, str(code))
    requests_mock.get(url, status_code=code)
    with pytest.raises(Exception):
        assert download(url, tmp_path)
