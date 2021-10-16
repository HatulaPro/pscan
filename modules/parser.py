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

    args = parser.parse_args()
    return args
