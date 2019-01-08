import re
import requests
import time
from bs4 import BeautifulSoup

#t0 = time.time()
#hrefs = re.compile('^/01觀點/[0-9]+')
urls = dict()
html = requests.get('https://www.hk01.com/tag/8502').text
soup = BeautifulSoup(html,'html.parser')
for x in soup('a'):
    if '/01觀點/' in x.get('href',None):
        urls[x.get('href',None)] = urls.get(x.get('href',None),1)
for url in urls:
    print('https://www.hk01.com{}'.format(url))
#print(time.time()-t0)
