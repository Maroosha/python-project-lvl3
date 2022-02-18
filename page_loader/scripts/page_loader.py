"Script for page loader."

# !usr/bin/env python3

import argparse
import logging
import sys
from page_loader.page_loader import download

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
    except Exception as some_error:
        logging.error(some_error)
        print('ATTENTION: An unexpected error occured. \
            For details, see %s.', LOG_FILE)
        sys.exit(100500)


if __name__ == '__main__':
    main()
