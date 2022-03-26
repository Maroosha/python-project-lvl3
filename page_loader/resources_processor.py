"Auxilary resources processing functions for page_loader.py."

import logging
import os
import page_loader.io_functions as functions
import page_loader.url as url_
import typing
from pathlib import Path
from progress.bar import IncrementalBar
from urllib.parse import urlparse


TAG_ATTRIBUTE_DICT = {'img': 'src', 'link': 'href', 'script': 'src'}


def get_resources(
    tag: str,
    soup: str,
    webpage_url: str,
) -> typing.Tuple[str, str]:
    """Get resource info.

    Parameters:
        tag: 'img', 'link' or 'script',
        soup: bs4-ed webpage contents,
        website_url: website url.

    Returns:
        resources from bs4 and sources of image paths.
    """
    paths = []
    resources = soup.find_all(tag)
    for resource in resources:
        attribute = resource.get(TAG_ATTRIBUTE_DICT[tag])
        if url_.is_local(attribute, webpage_url):
            paths.append(attribute)
    return resources, paths


def download_resource(
    url: str,
    path_to_directory: str,
    resource_paths: list,
) -> typing.List[str]:
    """Download resources from 'image', 'link', 'scripts' tag.

    Parameters:
        url: website url,
        path_to_directory: path to the dir where the resource will be stored,
        resource_paths: list of resources.

    Returns:
        list of relative pathes to links.
    """
    relative_paths = []
    for resource in resource_paths:
        url_core = url_.prepare_url(url)
        logging.debug(f'Downloading {url_core + resource}')
        filename = get_resource_name(url_core, resource)
        bar_ = IncrementalBar(f'{filename}', max=1, suffix='%(percent)d%%')
        filepath = os.path.join(path_to_directory, filename)
        try:
            data, flag = url_.get_resource_data(url_core, resource)
            functions.write_to_file(filepath, data, flag)
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
            f'{url_.get_directory_name(url)}/{filename}'
        )
        bar_.next()
        relative_paths.append(relative_path_to_link)
        bar_.finish()
    return relative_paths


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
        suffix = Path(resource).suffix
    else:  # src = '/assets/professions/nodejs'
        src = resource
        suffix = '.html'
    if resource_parse.scheme:
        src = src[len(resource_parse.scheme) + 3:]
        name = url_.hyphenate(src)  # -assets-professions-nodejs
        resource_name = name + suffix
    else:
        name = url_.hyphenate(src)  # -assets-professions-nodejs
        resource_name = url_.get_website_name(url) + name + suffix
    return resource_name


def replace_paths(
    tag: str,
    resources: typing.List[str],
    paths: typing.List[str],
    relative_paths: typing.List[str],
):
    """Replace paths to resources with their relative paths.

    Parameters:
        tag: 'img', 'link' or 'script',
        resources: bs4-ed resource (image/link/source),
        paths: path to the resource,
        relative_paths: relative paths to the resource.
    """
    path_to_relative_path = dict(zip(paths, relative_paths))
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
    resources, paths = get_resources(tag, soup, url)
    logging.debug(f'Sources {tag} are being downloaded...')
    relative_paths = download_resource(
        url,
        path_to_files,
        paths,
    )
    logging.info(f'Sources {tag} successfully downloaded.')
    replace_paths(
        tag,
        resources,
        paths,
        relative_paths,
    )
