import requests
import datetime
import json
import sys
import argparse
from bs4 import BeautifulSoup
from dateutil.parser import parse

websites = {'undercoverEconomist': ['http://timharford.com/articles/undercovereconomist', 'div', {'id': 'content-inner'},
                                    'h2', 'a', {'class': 'date'}],
            'moneyness': ['http://jpkoning.blogspot.com', 'div', {'class': 'blog-posts hfeed'},
                          'h3', 'h2', {'class': 'date-header'}],
            'angryBear': ['https://angrybearblog.com', 'section', {'id': 'main'},
                          'h2', 'span', {'class': 'separator'}],
            'truthOnTheMarket': ['https://truthonthemarket.com', 'div', {'id': 'main'},
                                 'h2', 'span', {'class': 'the-time updated'}],
            'libertyStreetEconomics': ['http://libertystreeteconomics.newyorkfed.org', 'div', {'class': 'grid_6 push_1'},
                                       'h3', 'div', {'class': 'ts-blog-strap'}],
            'voxEU': ['http://voxeu.org', 'div', {'class': 'view-content'},
                      'h2', 'span', {'class': 'date-display-single'}],
            #'cepr': ['http://cepr.net/blogs/cepr-blog', 'div', {'class': 'blog'},
            #         'h2', 'dd', {'class': 'published'}],
            'nber': ['http://www.nber.org', 'div', {'id': 'storyWrapper'},
                     'h2', 'p', {'class': 'subheadSource'}],
            'calculatedRisk': ['http://www.calculatedriskblog.com/', 'div', {'class': 'blog-posts hfeed'},
                               'h3', 'abbr', {'class': 'published'}]
            }

with open('rss.json', 'r') as f:
    titleAndLinks = json.load(f)

soup = ''


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.BOLD = ''
        self.UNDERLINE = ''


def url(website):
    global soup
    url = website[0]
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def link(name, website, soup):
    results = soup.find(website[1], website[2])
    links = results.find_all(website[3])

    for item in links:
        try:
            item_text = item.find('a').text
            item_href = item.find('a').attrs['href']
        except:
            pass

        if website[0] == 'http://cepr.net/blogs/cepr-blog/':
            item_href = 'http://cepr.net' + item_href

        if item_href[0] != 'h':
            item_href = website[0] + item_href

        if item_text and item_href:
            if item_text in titleAndLinks[name]['title']:
                pass
            else:
                titleAndLinks[name].setdefault('title', []).append(item_text)
                titleAndLinks[name].setdefault('link', []).append(item_href)

    return titleAndLinks


def date(name, website, soup):
    results = soup.find(website[1], website[2])
    dates = results.find_all(website[4], website[5])
    for d in dates:
        try:
            d_text = d.text
        except:
            pass

        try:
            #titleAndLinks[name].setdefault('date', []).append(parse(d_text))
            print(parse(d_text))
        except Exception as e:
            print('this one is not the right format' + name + d_text, e)


def websiteLoop():
    for k in websites.keys():
        url(websites[k])
        link(k, websites[k], soup)
        date(k, websites[k], soup)


def main():
    websiteLoop()
    #for k, v in titleAndLinks.items():
    #    print(bcolors.BOLD + k.strip() + bcolors.ENDC)
    #    print(bcolors.UNDERLINE + bcolors.OKBLUE + v + bcolors.ENDC)
    #    print('\n')
    with open('rss.json', 'w') as f:
        json.dump(titleAndLinks, f, indent=4)


if __name__ == '__main__':
    main()

