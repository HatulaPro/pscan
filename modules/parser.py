import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='A website scanner to find pages on a given url.')
    parser.add_argument('--url', metavar='URL', type=str,
                        required=True, help='The url to scan. Format: schema://IP/')

    args = parser.parse_args()
    return args
