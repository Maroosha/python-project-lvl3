"Download a webpage into a folder."

import logging
import os
import page_loader.io_functions as functions
import page_loader.helper as helper
from bs4 import BeautifulSoup


def download(url, directory_path=os.getcwd()):
    """Get path to file with a saved webpage.

    Parameters:
        dir_path: path to a directory with downloaded webpage,
        url: url of a webpage to be downloaded.
    """
    webpage_data = helper.get_webpage_contents(url)
    logging.debug('Webpage contents retrieved.')
    html_filename = helper.get_main_file_name(helper.get_name(url))
#    if directory_path == '.':
#        directory_path = os.getcwd()
    html_filepath = os.path.join(directory_path, html_filename)
    logging.info(f'Webpage {url} contents will be stored in {html_filepath}.')

    directory_with_files = helper.get_directory_name(helper.get_name(url))
    path_to_files = os.path.join(directory_path, directory_with_files)
    try:
        os.mkdir(path_to_files)
    except FileNotFoundError as not_found:
        print(f'No such file or directory: {path_to_files}')
        logging.exception('No such file or directory: %s', path_to_files)
        raise not_found
    except OSError as err:
        print(f'Directory {path_to_files} already exists.')
        logging.exception(
            'Directory %s since exists.',
            path_to_files,
        )
        raise err
    logging.info('Downloaded files will be stored in %s.', path_to_files)

    soup = BeautifulSoup(webpage_data, 'html.parser')
    logging.debug('Webpage contents is being parsed...')

    helper.process_source('img', path_to_files, soup, url)
    helper.process_source('link', path_to_files, soup, url)
    helper.process_source('script', path_to_files, soup, url)

    functions.write_to_file(html_filepath, soup.prettify())
    logging.info('Webpage contents successfully saved in %s.', html_filepath)

    return html_filepath
