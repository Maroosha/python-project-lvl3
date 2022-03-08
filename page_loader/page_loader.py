"Download a webpage into a folder."

import logging
import os
import page_loader.functions as functions
from bs4 import BeautifulSoup


def download(url, directory_path='current'):
    """Get path to file with a saved webpage.

    Parameters:
        dir_path: path to a directory with downloaded webpage,
        url: url of a webpage to be downloaded.
    """
    webpage_content = functions.get_webpage_contents(url)
    logging.debug('Webpage contents retrieved.')
    filename = functions.get_main_file_name(functions.get_name(url))
    if directory_path == 'current':
        directory_path = os.getcwd()
    filepath = os.path.join(directory_path, filename)
    logging.info(f'Webpage {url} contents will be stored in {filepath}.')

    # create a dicrecotry for files
    directoryname_files = functions.get_directory_name(functions.get_name(url))
    directorypath_files = os.path.join(directory_path, directoryname_files)
    try:
        os.mkdir(directorypath_files)  # path/to/webpage-url_files
    except FileNotFoundError as not_found:
        print(f'No such file or directory: {directorypath_files}')
        logging.exception('No such file or directory: %s', directorypath_files)
        raise not_found
    except OSError as err:
        print(f'Directory {directorypath_files} already exists.')
        logging.exception(
            'Directory %s since exists.',
            directorypath_files,
        )
        raise err
    logging.info('Downloaded files will be stored in %s.', directorypath_files)

    # parse webpage contents
    file_contents = BeautifulSoup(webpage_content, 'html.parser')
    logging.debug('Webpage contents is being parsed...')
    logging.debug(f'Webpage contents: {file_contents.prettify()}')
    images, list_of_images = functions.get_images(file_contents)
    links, list_of_links = functions.get_links(file_contents, url)
    scripts, list_of_scripts = functions.get_scripts(file_contents, url)

    # download all the files and return list of pathes to them:
    logging.debug('Images are being downloaded...')
    list_of_image_relative_pathes = functions.download_image(
        url,
        directorypath_files,
        list_of_images,
    )
    logging.debug(f'list_of_image_relative_pathes: \
{list_of_image_relative_pathes}')
    logging.info('Images successfully downloaded.')
    logging.debug('Sources are being downloaded...')  # links???
    list_of_links_relative_pathes = functions.download_link(
        url,
        directorypath_files,
        list_of_links,
    )
    logging.debug(f'list_of_links_relative_pathes: \
{list_of_links_relative_pathes}')
    logging.info('Sources successfully downloaded.')  # or links???
    logging.debug('Scripts are being downloaded...')
    list_of_scripts_relative_pathes = functions.download_script(
        url,
        directorypath_files,
        list_of_scripts,
    )
    logging.debug(f'list_of_scripts_relative_pathes: \
{list_of_scripts_relative_pathes}')
    logging.info('Scripts successfully downloaded.')

    # replace relative pathes (imgs, links, scripts[src]) in webpage contents
    functions.replace_image_pathes(
        images,
        list_of_images,
        list_of_image_relative_pathes,
    )
    functions.replace_pathes(
        links,
        list_of_links,
        list_of_links_relative_pathes,
        'href',
    )
    functions.replace_pathes(
        scripts, list_of_scripts, list_of_scripts_relative_pathes, 'src',
    )

    logging.debug(f'File contents will be {file_contents.prettify()}')

    functions.write_to_file(filepath, file_contents.prettify())
    logging.info('Webpage contents successfully saved in %s.', filepath)

    print(f'\nPage was successfully downloaded into {filename}')
    return filepath
