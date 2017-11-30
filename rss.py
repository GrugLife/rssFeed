import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse

websites = {'angryBear': ['https://angrybearblog.com', 'section', {'id': 'main'},
                          'h2', 'p', {'class': 'postmetadata'}]}
url = websites['angryBear'][0]
r = requests.get(url)
r.raise_for_status()
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find(websites['angryBear'][1], websites['angryBear'][2])
date = results.find_all(websites['angryBear'][4], websites['angryBear'][5])
dateList = []
today = datetime.datetime.now()
DD = datetime.timedelta(days=7)
lookBack = today - DD
for d in date:
    if len(d.text.split('|')) == 2:
        print(parse(d.text.split('|')[1]) > lookBack)







