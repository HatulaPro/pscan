import requests
from modules import parser
from modules.logger import Logger
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunsplit, urlsplit, urljoin


VERSION = '1.0.1v'

history = []

config = {
    'URL': None,
    'bad_status_codes': [404],
    'REDIRECTS': False
}


def drop_params(url):
    '''
    Removes URL query parameters.
    '''
    return urlunsplit(urlsplit(url)._replace(query="", fragment=""))


def get_paths_from_robots(url):
    '''
    Finds `/robots.txt` file, parses it and returns all the URLs there.
    '''
    res = requests.get(urljoin(url, '/robots.txt'))
    if res.status_code == 404:
        Logger.error('Can not find `/robots.txt` file.')
        return []
    else:
        Logger.message('Found `/robots.txt` file. Starting scan.')
        result = []
        lines = res.text.split('\n')
        for line in lines:
            if line.startswith('Allow') or line.startswith('Disallow'):
                result.append(line.split(' ')[1].strip())
        return result


def scan(url, depth=0):
    '''
    Recuresivly search for links and sources in a site
    depends on the global configuration
    '''
    if url in history:
        return
    elif depth > config['DEPTH']:
        return

    res = requests.get(url, allow_redirects=config['REDIRECTS'])
    if res.status_code not in config['bad_status_codes']:
        # If redirected
        if res.url != url:
            history.append(res.url)
            Logger.info(
                f"Found [{url}] -> [{res.url}] ({res.status_code}) - size={len(res.text)} depth={depth}")
        else:
            Logger.info(
                f"Found [{url}] ({res.status_code}) - size={len(res.text)} depth={depth}")
        history.append(url)

        # Find a tags in html
        html = BeautifulSoup(res.text, 'html.parser')
        links = list(dict.fromkeys([drop_params(link.get('href')) for link in html.find_all()
                                    if link.name == 'a' and link.get('href')]))

        # Find static files
        if config['STATIC']:
            static_link_tags = [drop_params(link.get('href')) for link in html.find_all()
                                if link.name == 'link' and link.get('href')]
            static_script_tags = [drop_params(link.get('src')) for link in html.find_all()
                                  if link.name == 'script' and link.get('src')]
            static_img_tags = [drop_params(link.get('src')) for link in html.find_all()
                               if link.name == 'img' and link.get('src')]
            static_links = list(dict.fromkeys(
                static_link_tags + static_script_tags + static_img_tags))
            for static_link in static_links:
                Logger.info(
                    f"Found static source [{urljoin(url, static_link)}] - depth={depth}")

        # Recursion
        for link in links:
            url_to_scan = urljoin(url, link)
            parsed = urlparse(url_to_scan)
            if parsed.scheme in ['http', 'https'] and parsed.netloc == config['URL'].netloc:
                scan(url_to_scan, depth=depth+1)


def main():
    args = parser.get_args()
    try:
        config['URL'] = urlparse(args.url)
        URL = config['URL'].geturl()
        # Schema must be either http or https
        assert config['URL'].scheme in [
            'http', 'https'], f"Invalid schema: {config['URL'].scheme}"

        config['DEPTH'] = args.depth
        config['REDIRECTS'] = args.follow_redirects
        config['STATIC'] = args.static

        # Setting logger
        Logger.set_output_file(args.output_file)
        Logger.message(
            f"pscan {VERSION}\n    url: {URL}\n    depth: {config['DEPTH']}")
        Logger.message(f'github: https://github.com/HatulaPro/pscan\n\n')

        # Scanning robots file if robots flag is set
        if args.robots:
            paths = get_paths_from_robots(URL)
            for path in paths:
                Logger.message(f'Scanning robots path `{path}`')
                scan(urljoin(URL, path))

        Logger.message('Starting scan')
        scan(URL)
        Logger.message('Done.')

    except KeyboardInterrupt as e:
        Logger.error('Program stopped.')
    except Exception as e:
        Logger.error(e)


if __name__ == '__main__':
    main()
