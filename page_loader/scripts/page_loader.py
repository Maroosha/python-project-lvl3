"Script for page loader."

# !usr/bin/env python3

import argparse
from page_loader.page_loader import download


def main():
    parser = argparse.ArgumentParser(description='Webpage loader')
    parser.add_argument(
        '--output',
        default='current',  # current working directory
        help='directory path',
    )
    parser.add_argument('url')
    args = parser.parse_args()
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
