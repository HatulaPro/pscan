import requests
from modules import parser


def main():
    args = parser.get_args()
    print(args.url)


if __name__ == '__main__':
    main()
