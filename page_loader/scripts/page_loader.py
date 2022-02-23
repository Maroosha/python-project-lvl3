"Script for page loader."

# !usr/bin/env python3

import argparse
import logging
import sys
from page_loader.page_loader import download
from page_loader.page_loader import KnownError

LOG_FILE = 'page_loader.log'


def main():
    "."
    parser = argparse.ArgumentParser(description='Webpage loader')
    parser.add_argument(
        '--output',
        default='current',  # current working directory
        help='directory path',
    )
    parser.add_argument('url')
    args = parser.parse_args()
    try:
        download(args.url, args.output)
    except IOError as unknown_error:
        logging.error(unknown_error)
        print('ATTENTION: An unexpected error occured. \
For details, see %s.', LOG_FILE)
        sys.exit(1)
    except KnownError as known_error:
        logging.error(known_error)
        print('ATTENTION: An error occured: %s.', known_error)
        sys.exit(1)


if __name__ == '__main__':
    main()
