#!/usr/bin/env python

import os
import requests
from bs4 import BeautifulSoup

url = 'http://www.stateair.net/web/post/1/2.html'


html = requests.get(url,timeout=3)
soup = BeautifulSoup(html.text)

result = soup.find_all("div",class_="span-5 last currentExposure")

a = result[0].contents[1].text.replace('\t','')

print a


