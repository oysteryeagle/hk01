import requests
from bs4 import BeautifulSoup
import re

html = requests.get('https://www.hk01.com/tag/8502').text
soup = BeautifulSoup(html,'html.parser')
for text in soup('script',text=True):
    nextOffset = re.findall('''"nextOffset":([0-9]{2,})''',str(text))
    for firstOffsetValue in nextOffset:
        if firstOffsetValue != '[]':
            #print(value)
            #url = 'https://web-data.api.hk01.com/v2/feed/tag/8502?offset={}&bucketId=00000'.format(value)
            #print(url)
            return firstOffsetValue
