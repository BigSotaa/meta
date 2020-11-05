import string
import re


class parser:
    def __init__(self, results, word=""):
        self.results = results
        self.word = word
        self.temp = []

    def genericClean(self):
        if isinstance(self.results, bytes):
            self.results = self.results.decode('utf-8')
        self.results = re.sub('<em>', '', self.results)
        self.results = re.sub('<b>', '', self.results)
        self.results = re.sub('</b>', '', self.results)
        self.results = re.sub('</em>', '', self.results)
        self.results = re.sub('%2f', ' ', self.results)
        self.results = re.sub('%3a', ' ', self.results)
        self.results = re.sub('<strong>', '', self.results)
        self.results = re.sub('</strong>', '', self.results)
        self.results = re.sub('<w:t>', ' ', self.results)

        for e in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C'):
            self.results = self.results.replace(e, ' ')

    def urlClean(self):
        self.results = re.sub('<em>', '', self.results)
        self.results = re.sub('</em>', '', self.results)
        self.results = re.sub('%2f', ' ', self.results)
        self.results = re.sub('%3a', ' ', self.results)
        for e in ('<', '>', ':', '=', ';', '&', '%3A', '%3D', '%3C'):
            self.results = self.results.replace(e, ' ')

    def emails(self):
        self.genericClean()
        reg_emails = re.compile('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
        self.temp = reg_emails.findall(self.results)
        emails = self.unique()
        return emails

    def fileurls(self):
        urls = []
        reg_urls = re.compile('<a href="(.*?)"')
        self.temp = reg_urls.findall(self.results.decode('utf-8'))
        allurls = self.unique()
        for z in allurls:
            y = z.replace('/url?q=', '')
            x = y.split('&')[0]
            if any(k in x for k in ['webcache','google.com']) or not x.startswith("http") or self.word not in x:
                pass
            else:
                urls.append(x)
        return urls

    def people_linkedin(self):
        reg_people = re.compile('">[a-zA-Z0-9._ -]* profiles | LinkedIn')

        self.temp = reg_people.findall(self.results)
        resul = []
        for x in self.temp:
            y = x.replace('  LinkedIn', '')
            y = y.replace(' profiles ', '')
            y = y.replace('LinkedIn', '')
            y = y.replace('"', '')
            y = y.replace('>', '')
            if y != " ":
                resul.append(y)
        return resul

    def profiles(self):
        reg_people = re.compile('">[a-zA-Z0-9._ -]* - <em>Google Profile</em>')
        self.temp = reg_people.findall(self.results)
        resul = []
        for x in self.temp:
            y = x.replace(' <em>Google Profile</em>', '')
            y = y.replace('-', '')
            y = y.replace('">', '')
            if y != " ":
                resul.append(y)
        return resul

    def hostnames(self):
        self.genericClean()
        reg_hosts = re.compile('[a-zA-Z0-9.-]*\.' + self.word)
        self.temp = reg_hosts.findall(self.results)
        hosts = self.unique()
        return hosts

    def hostnames_all(self):
        reg_hosts = re.compile('<cite>(.*?)</cite>')
        temp = reg_hosts.findall(self.results)
        for x in temp:
            if x.count(':'):
                res = x.split(':')[1].split('/')[2]
            else:
                res = x.split("/")[0]
            self.temp.append(res)
        hostnames = self.unique()
        return hostnames

    def unique(self):
        self.new = []
        for x in self.temp:
            if x not in self.new:
                self.new.append(x)
        return self.new
