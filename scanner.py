import requests
from modules import parser
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urlparse, urlunsplit, urlsplit, urljoin


VERSION = '1.0.1v'

history = []

config = {
    'URL': None,
    'bad_status_codes': [404]
}


def drop_params(url):
    return urlunsplit(urlsplit(url)._replace(query="", fragment=""))


def scan(url, depth=0):
    if url in history:
        return
    elif depth > config['DEPTH']:
        return

    res = requests.get(url)
    if res.status_code not in config['bad_status_codes']:
        print(f"Found [{url}] ({res.status_code}) - depth={depth}")
        history.append(url)

        html = BeautifulSoup(res.text, 'html.parser')
        links = list(dict.fromkeys([drop_params(link.get('href')) for link in html.find_all()
                                    if link.name == 'a' and link.get('href')]))
        # pprint(links)
        for link in links:
            url_to_scan = urljoin(url, link)
            parsed = urlparse(url_to_scan)
            if parsed.scheme in ['http', 'https'] and parsed.netloc == config['URL'].netloc:
                scan(url_to_scan, depth=depth+1)


def main():
    args = parser.get_args()
    try:

        config['URL'] = urlparse(args.url)
        assert config['URL'].scheme in [
            'http', 'https'], f"Invalid schema: {config['URL'].scheme}"

        config['DEPTH'] = args.depth

        print(
            f"Starting pscan {VERSION}\n    url: {config['URL'].geturl()}\n    depth: {config['DEPTH']}\n")

        scan(config['URL'].geturl())
    except KeyboardInterrupt as e:
        print('Program stopped.')
    except Exception as e:
        pprint(e)


if __name__ == '__main__':
    main()
