import argparse


DEFAULT_DEPTH = 5


def get_args():
    parser = argparse.ArgumentParser(
        description='A website scanner to find pages on a given url.')
    parser.add_argument('-u', '--url', metavar='URL', type=str,
                        required=True, help='The url to scan. Format: schema://IP/')
    parser.add_argument('-d', '--depth', metavar='depth', type=int,
                        default=DEFAULT_DEPTH, help=f'The depth of the scan. Default: {DEFAULT_DEPTH}')

    parser.add_argument('-o', '--output-file', metavar='file-name', type=str,
                        default=None, help=f'File to output to. Default: None')

    parser.add_argument('-r', '--robots', action='store_true',
                        help=f'Add this flag to scan `robots.txt`.')
    parser.add_argument('-f', '--follow-redirects', action='store_true',
                        help=f'Add this flag to follow redirects.')
    parser.add_argument('-s', '--static', action='store_true',
                        help=f'Add this flag to scan for static non-html files.')

    args = parser.parse_args()
    return args
