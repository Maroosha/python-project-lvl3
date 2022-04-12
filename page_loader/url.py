"Auxilary url processing functions for page_loader.py."

from urllib.parse import urljoin, urlparse


class KnownError(Exception):
    "Some known error."
    pass


def hyphenate(string: str) -> str:
    """Replace non-numeric and non-literal characters with a hyphen.

    Parameters:
        string: string to be processed.

    Returns:
        hyphenated string.
    """
    return ''.join([
        '-' if not i.isalpha() and not i.isdigit() else i for i in string
    ])


def _get_name(url: str) -> str:
    """Derive a name of a directory or file from an url.

    Parameters:
        url: webpage url.

    Returns:
        directory or file name as a string.
    """
    parsed = urlparse(str(url))
    address = parsed.netloc + parsed.path
    return hyphenate(address)


def get_directory_name(url: str) -> str:
    """Get directory name containing downloaded webpage data.

    Parameters:
        url: webpage url.

    Returns:
        directory name as a string.
    """
    return _get_name(url) + '_files'


def get_website_name(url: str) -> str:
    """Get a name of a file containing downloaded webpage.

    Parameters:
        url: webpage url.

    Returns:
        name of a file containing the downloaded webpage.
    """
    parsed = urlparse(str(url)).netloc
    return hyphenate(parsed)


def get_html_file_name(url: str) -> str:
    """Get a name of a file containing downloaded webpage.

    Parameters:
        url: webpage url.

    Returns:
        name of a file containing the downloaded webpage.
    """
    return _get_name(url) + '.html'


def prepare_url(url: str) -> str:
    """Get url in the form of scheme://netloc.

    Parameters:
        url: webpage url.

    Returns:
        url in the form of scheme://netloc.
    """
    parsed_url = urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.netloc


def is_local(url: str, webpage_url: str) -> bool:
    """Check whether a resource is local or not.

    Parameters:
        url: webpage url,
        webpage_url: url from src/href.

    Returns:
        true if local, false if not
    """
    parse_result = urlparse(str(url))
    webpage_netloc = urlparse(webpage_url).netloc
    return parse_result.netloc == webpage_netloc or parse_result.netloc == ''


def to_absolute(root_page_url: str, url: str) -> str:
    """Get an absolute url.

    Parameters:
        root_page_url: url in the form of scheme://netloc,
        url: resource link.

    Returns:
        absolute url.
    """
    return urljoin(root_page_url, url) if not urlparse(url).netloc else url
