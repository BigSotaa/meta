import random
import requests, sys
import myparser
from urllib.parse import urlencode
import time


class search_google:
    def __init__(self, domain_name, offset=0, results_limit=200, filetype="pdf"):
        self.domain_name = domain_name
        self.offset = offset
        self.results = b""
        self.totalresults = b""
        self.filetype = filetype
        self.server = "https://www.google.com"
        self.hostname = "www.google.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.quantity = "100"
        self.results_limit = results_limit
        self.counter = 0

    def do_search_files(self, offset, quantity):
        headers = {
            'Host': self.hostname,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': '',
            'Upgrade-Insecure-Requests': '1'
        }
        params = {
            "num": quantity,
            "start": offset,
            "hl": "en",
            "meta": "",
            "q": f"filetype:{self.filetype} site:{self.domain_name}"
        }

        print("Requested URL: " + self.server + "/search?" + urlencode(params))

        h = requests.get(self.server + "/search", params=params, headers=headers)
        if h.status_code != 200:
            print(f"An error occurred while requesting Google (Error code {h.status_code})")
            return
        self.totalresults += h.content

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.domain_name)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.domain_name)
        return rawres.hostnames()

    def get_files(self):
        rawres = myparser.parser(self.totalresults, self.domain_name)
        return rawres.fileurls()

    def process_files(self):
        while self.counter < self.results_limit:
            self.do_search_files(self.counter + self.offset, min(100, self.results_limit - self.counter))
            time.sleep(2)
            self.counter += 100
