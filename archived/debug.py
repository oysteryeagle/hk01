import requests
from bs4 import BeautifulSoup
import re

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

html = requests.get('https://www.hk01.com/01觀點/182819/01周報社論-發展高球場非仇商-社會整體利益為重').text
soup = BeautifulSoup(html,'html.parser')
time = soup('meta',attrs = {'property':'article:published_time'})
print(time.get('content').split('T')[0])
    #print(x.get('content',None) + '\n')
