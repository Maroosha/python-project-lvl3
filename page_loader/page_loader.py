"Download a webpage into a folder."

import logging
import os
import page_loader.io_functions as functions
import page_loader.url as url_
import page_loader.resources_processor as resproc
from bs4 import BeautifulSoup


def download(url: str, directory_path=os.getcwd()) -> str:
    """Get path to file with a saved webpage.

    Parameters:
        dir_path: path to a directory with downloaded webpage,
        url: url of a webpage to be downloaded.

    Returns:
        Path to html file with webpage data.
    """
    webpage_data = url_.get_webpage_data(url)
    logging.debug('Webpage contents retrieved.')
    html_filename = url_.get_html_file_name(url)
    html_filepath = os.path.join(directory_path, html_filename)
    logging.info(f'Webpage {url} contents will be stored in {html_filepath}.')

    directory_with_resourses = url_.get_directory_name(url)
    path_to_resourses = os.path.join(directory_path, directory_with_resourses)
    try:
        os.mkdir(path_to_resourses)
    except FileNotFoundError as not_found:
        print(f'No such file or directory: {path_to_resourses}')
        logging.exception('No such file or directory: %s', path_to_resourses)
        raise not_found
    except OSError as err:
        print(f'Directory {path_to_resourses} already exists.')
        logging.exception(
            'Directory %s since exists.',
            path_to_resourses,
        )
        raise err
    logging.info('Downloaded files will be stored in %s.', path_to_resourses)

    soup = BeautifulSoup(webpage_data, 'html.parser')
    logging.debug('Webpage contents is being parsed...')

    for tag in ['img', 'link', 'script']:
        resproc.process_resource(tag, path_to_resourses, soup, url)

    functions.write_to_file(html_filepath, soup.prettify())
    logging.info('Webpage contents successfully saved in %s.', html_filepath)

    return html_filepath
