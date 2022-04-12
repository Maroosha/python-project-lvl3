"Auxilary resources processing functions for page_loader.py."

import logging
import os
import page_loader.io_functions as functions
import page_loader.url as url_
import requests
from bs4.element import Tag
from pathlib import Path
from typing import List, Dict
from progress.bar import IncrementalBar
from urllib.parse import urlparse


TAG_ATTRIBUTE_DICT = {'img': 'src', 'link': 'href', 'script': 'src'}
TAGS = ('img', 'link')


def _get_link(resource: Tag) -> str:
    """Get link from Tag object.

    Parameters:
        resource: resource from a webpage.

    Returns:
        link from tag.
    """
    if resource.get('href'):
        return resource.get('href')
    return resource.get('src')


def _get_resources(
    resources: List[Tag],
    url: str,
) -> Dict[Tag, str]:
    """Get resource info.

    Parameters:
        resources: resources from bs4-ed url,
        url: website url.

    Returns:
        resources from bs4 and sources of image paths.
    """
    tag_to_link = {}
    for resource in resources:
        link = _get_link(resource)
        if url_.is_local(link, url) and link is not None:
            tag_to_link.update({resource: link})
    return tag_to_link


def _download_resource(
    url: str,
    path_to_directory: str,
    resource_paths: List[str],
) -> List[str]:
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
        filename = _get_resource_name(url_core, resource)
        bar_ = IncrementalBar(f'{filename}', max=1, suffix='%(percent)d%%')
        filepath = os.path.join(path_to_directory, filename)
        try:
            data = functions.get_resource_data(url_core, resource)
            functions.write_to_file(filepath, data)
            bar_.next()
        except url_.KnownError:
            print(f'An exception has occurred (see logs).')
            logging.error('KnownError has occurred.')
            continue
        except PermissionError as error1:
            print(f'Access denied to file {filepath}.')
            logging.error('Access denied to file %s.', filepath)
            raise error1
        except OSError as error2:
            print(f'Unable to save data to {filepath}.')
            logging.error('Unable to save data to %s.', filepath)
            raise error2
        except requests.RequestException as err:
            print(f'Unable to process {resource}')
            logging.info(err)
            logging.error('Unable to process %s', resource)
            continue
        relative_path_to_link = (
            f'{url_.get_directory_name(url)}/{filename}'
        )
        bar_.next()
        relative_paths.append(relative_path_to_link)
        bar_.finish()
    return relative_paths


def _get_resource_name(url: str, resource: str) -> str:
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


def _replace_paths(
    tag_to_link: Dict[Tag, str],
    relative_paths: List[str],
):
    """Replace paths to resources with their relative paths.

    Parameters:
        tag_to_link: path to the resource,
        relative_paths: relative paths to the resource.
    """
    for tag, local_file_link in zip(tag_to_link, relative_paths):
        tag[TAG_ATTRIBUTE_DICT[tag.name]] = local_file_link


def process_resources(
    path_to_resources: str,
    resource_tags: List[Tag],
    url: str,
):
    """
    Process a resource.

    Parameters:
        path_to_files: path to a directory with downloaded files,
        resource_tags: tags,
        url: webpage url.
    """
    tag_to_link = _get_resources(resource_tags, url)
    relative_paths = _download_resource(
        url,
        path_to_resources,
        tag_to_link.values(),
    )
    _replace_paths(
        tag_to_link,
        relative_paths,
    )
