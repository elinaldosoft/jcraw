from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import logging
from app.util import random_agent


class SpiderBase:
    name: str
    html: str
    url_base: str
    soup: BeautifulSoup

    def run(self, path, **kwargs) -> BeautifulSoup:
        self.request(path, **kwargs)
        self.soup = self.html_to_soup(**kwargs)
        return self.soup

    def request(self, path: str, **kwargs) -> str:
        try:
            url = urljoin(self.url_base, path)
            response = requests.get(url, headers={'User-Agent': random_agent()}, **kwargs)
            response.raise_for_status()
            self.html = response.text
        except requests.exceptions.HTTPError as err:
            logging.exception(err)
        return self.html

    def html_to_soup(self, html: str = None, parser: str = 'html.parser') -> BeautifulSoup:
        return BeautifulSoup(html or self.html, parser)
