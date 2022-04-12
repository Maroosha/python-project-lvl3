"Download a webpage into a folder."

import logging
import os
import page_loader.io_functions as functions
import page_loader.url as url_
import page_loader.resources_processor as resproc
from bs4 import BeautifulSoup


TAGS = ('img', 'link', 'script')


def download(url: str, directory_path: str = os.getcwd()) -> str:
    """Get path to file with a saved webpage.

    Parameters:
        dir_path: path to a directory with downloaded webpage,
        url: url of a webpage to be downloaded.

    Returns:
        Path to html file with webpage data.
    """
    webpage_data = functions.get_webpage_data(url)
    logging.debug('Webpage contents retrieved.')
    html_filename = url_.get_html_file_name(url)
    html_filepath = os.path.join(directory_path, html_filename)
    logging.info(f'Webpage {url} contents will be stored in {html_filepath}.')

    directory_with_resourses = url_.get_directory_name(url)
    path_to_resources = os.path.join(directory_path, directory_with_resourses)
    try:
        os.mkdir(path_to_resources)
    except FileNotFoundError as not_found:
        logging.exception('No such file or directory: %s', path_to_resources)
        raise not_found
    except OSError as err:
        logging.exception(
            'Directory %s since exists.',
            path_to_resources,
        )
        raise err
    logging.info('Downloaded files will be stored in %s.', path_to_resources)

    soup = BeautifulSoup(webpage_data, 'html.parser')
    logging.debug('Webpage contents is being parsed...')
    resource_tags = soup.find_all(TAGS)
    logging.debug('Sources are being downloaded...')
    resproc.process_resources(path_to_resources, resource_tags, url)
    logging.info('Sources successfully downloaded.')

    functions.write_to_file(html_filepath, soup.prettify())
    logging.info('Webpage contents successfully saved in %s.', html_filepath)

    return html_filepath
