import requests
from bs4 import BeautifulSoup
import re

#pattern = re.compile(r'^/\w+')
pattern = re.compile(r'^/[0-9]*[\u4e00-\u9fff]+') #format for chinese characters
for x in range(1,30):
    urls = list()
    html = requests.get('https://www.hk01.com/tag/{}'.format(x)).text
    soup = BeautifulSoup(html,'html.parser')
    for tag in soup('a'):
    #    print(tag.get('href'))
        if tag.get('href',None) != None:
            if re.match(pattern,tag.get('href')):
                if 'https://www.hk01.com/tag{}'.format(tag.get('href')) not in urls: #store url into the list if url not already in the list
                    urls.append('https://www.hk01.com/tag{}'.format(tag.get('href')))
#urls is a list of urls found on the main page
