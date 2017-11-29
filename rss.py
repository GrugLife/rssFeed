import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse

websites = {'undercoverEconomist': ['http://timharford.com/articles/undercovereconomist', 'div', {'id': 'content-inner'},
                                    'h2', 'a', {'class': 'date'}]}
url = websites['undercoverEconomist'][0]
r = requests.get(url)
r.raise_for_status()
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find(websites['undercoverEconomist'][1], websites['undercoverEconomist'][2])
date = results.find_all(websites['undercoverEconomist'][4], websites['undercoverEconomist'][5])
dateList = []
for d in date:
    dateList.append(d.text)


#print([parse(d) for d in dateList])
print(parse(dateList[0]) < datetime.datetime.now())



