"Script for page loader."

# !usr/bin/env python3

import argparse
import logging
import sys
from page_loader.page_loader import download
from page_loader.functions import KnownError

LOG_FILE = 'page_loader.log'
FINAL_MESSAGE = '\nPage was successfully downloaded into {}'


def main():
    "."
    parser = argparse.ArgumentParser(description='Webpage loader')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0',
    )
    parser.add_argument(
        '-o', '--output',
        default='current',  # current working directory
        help='directory path',
    )
    parser.add_argument('url')
    args = parser.parse_args()
    try:
        filepath = download(args.url, args.output)
    except KnownError as known_error:
        logging.error(known_error)
        print('ATTENTION: An error occured: %s.', known_error)
        sys.exit(1)
    except Exception as unknown_error:
        logging.error(unknown_error)
        print('ATTENTION: An unexpected error occured. \
For details, see %s.', LOG_FILE)
        sys.exit(1)
    else:
        final_message = FINAL_MESSAGE.format(filepath)
        print(final_message)
        logging.info(final_message)
        sys.exit(0)


if __name__ == '__main__':
    main()
