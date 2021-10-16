import requests
from modules import parser
from modules.logger import Logger
from bs4 import BeautifulSoup
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
        Logger.info(
            f"Found [{url}] ({res.status_code}) - size={len(res.text)} depth={depth}")
        history.append(url)

        html = BeautifulSoup(res.text, 'html.parser')
        links = list(dict.fromkeys([drop_params(link.get('href')) for link in html.find_all()
                                    if link.name == 'a' and link.get('href')]))
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

        Logger.set_output_file(args.output_file)

        Logger.message(
            f"Starting pscan {VERSION}\n    url: {config['URL'].geturl()}\n    depth: {config['DEPTH']}\n")

        scan(config['URL'].geturl())

        Logger.message('Done.')
    except KeyboardInterrupt as e:
        Logger.error('Program stopped.')
    except Exception as e:
        Logger.error(e)


if __name__ == '__main__':
    main()
