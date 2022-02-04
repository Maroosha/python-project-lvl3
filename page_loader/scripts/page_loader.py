"Script for page loader."

# !usr/bin/env python3

import argparse
from page_loader.page_loader import download


def main():
    parser = argparse.ArgumentParser(description='Webpage loader.')
    parser.add_argument(
        '--output',
        default='current',  # current working directory
        help='download a webpage on your computer',
    )
    parser.add_argument('url')
    args = parser.parse_args()
    print(download(args.output, args.url))


if __name__ == '__main__':
    main()
