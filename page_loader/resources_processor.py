"Auxilary resources processing functions for page_loader.py."

import logging
import os
import page_loader.io_functions as functions
import page_loader.namer as namer
import page_loader.url_processor as urlproc
from pathlib import Path
from progress.bar import IncrementalBar
from urllib.parse import urlparse


TAG_ATTRIBUTE_DICT = {'img': 'src', 'link': 'href', 'script': 'src'}


def get_resources(tag: str, soup: str, webpage_url: str) -> tuple:
    """Get resource info.

    Parameters:
        tag: 'img', 'link' or 'script',
        soup: bs4-ed webpage contents,
        website_url: website url.

    Returns:
        resources from bs4 and sources of image pathes.
    """
    pathes = []
    resources = soup.find_all(tag)
    for resource in resources:
        attribute = resource.get(TAG_ATTRIBUTE_DICT[tag])
        if urlproc.is_local(attribute, webpage_url):
            if tag == 'script':
                if resource['src']:
                    pathes.append(attribute)
            pathes.append(attribute)
    return resources, pathes


def download_resource(url: str, path_to_directory: str, pathes: list) -> list:
    """Download resources from 'image', 'link', 'scripts' tag.

    Parameters:
        url: website url,
        path_to_directory: path to the dir where the resource will be stored,
        pathes: list of resources.

    Returns:
        list of relative pathes to links.
    """
    relative_pathes = []
    for resource in pathes:
        url_core = urlproc.prepare_url(url)
        logging.debug(f'Downloading {url_core + resource}')
        filename = get_resource_name(url_core, resource)
        bar_ = IncrementalBar(f'{filename}', max=1, suffix='%(percent)d%%')
        filepath = os.path.join(path_to_directory, filename)
        try:
            functions.write_resource_data_to_file(url_core, resource, filepath)
            bar_.next()
        except PermissionError as error1:
            print(f'Access denied to file {filepath}.')
            logging.error('Access denied to file %s.', filepath)
            raise error1
        except OSError as error2:
            print(f'Unable to save data to {filepath}.')
            logging.error('Unable to save data to %s.', filepath)
            raise error2
        relative_path_to_link = (
            f'{namer.get_directory_name(url)}/{filename}'
        )
        bar_.next()
        relative_pathes.append(relative_path_to_link)
        bar_.finish()
    return relative_pathes


def get_resource_name(url: str, resource: str) -> str:
    """Get name of the link/script resource (filename).

    Parameters:
        url: website url,
        resource: resource link.

    Returns:
        name of the resource.
    """
    resource_parse = urlparse(resource)
    if Path(resource).suffix:  # link = '/assets/professions/nodejs.png'
        src = resource[:-len(Path(resource).suffix)]
        print(f'src = {src}')
        suffix = Path(resource).suffix
    else:  # src = '/assets/professions/nodejs'
        src = resource
        suffix = '.html'
    if resource_parse.scheme:
        src = src[len(resource_parse.scheme) + 3:]
        name = ''.join([
            '-' if not i.isalpha() and not i.isdigit() else i for i in src
        ])  # -assets-professions-nodejs
        resource_name = name + suffix
    else:
        print('HERE 4')
        name = ''.join([
            '-' if not i.isalpha() and not i.isdigit() else i for i in src
        ])  # -assets-professions-nodejs
        resource_name = namer.get_website_name(url) + name + suffix
    return resource_name


def replace_pathes(
    tag: str,
    resources: list,
    pathes: list,
    relative_pathes: list,
):
    """Replace pathes to resources with their relative pathes.

    Parameters:
        tag: 'img', 'link' or 'script',
        resources: bs4-ed resource (image/link/source),
        pathes: path to the resource,
        relative_pathes: relative pathes to the resource.
    """
    path_to_relative_path = dict(zip(pathes, relative_pathes))
    for resource in resources:
        attr = resource.get(TAG_ATTRIBUTE_DICT[tag])
        if attr in path_to_relative_path:
            resource[TAG_ATTRIBUTE_DICT[tag]] = \
                path_to_relative_path[resource[TAG_ATTRIBUTE_DICT[tag]]]


def process_resource(tag: str, path_to_files: str, soup: str, url: str):
    """
    Process a resource.

    Parameters:
        tag: "img", "link", "script",
        path_to_files: path to a directory with downloaded files,
        soup: bs4-ed webpage contents,
        url: webpage url.
    """
    resources, pathes = get_resources(tag, soup, url)
    logging.debug(f'Sources {tag} are being downloaded...')
    relative_pathes = download_resource(
        url,
        path_to_files,
        pathes,
    )
    logging.info(f'Sources {tag} successfully downloaded.')
    replace_pathes(
        tag,
        resources,
        pathes,
        relative_pathes,
    )
