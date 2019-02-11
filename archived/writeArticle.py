import requests
from bs4 import BeautifulSoup
import re

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

html = requests.get('https://www.hk01.com/01觀點/271757/01周報社論-孟晚舟讓人看清美國-美國卻尚未看清自己').text
soup = BeautifulSoup(html,'html.parser')

f = open('testing.txt','w+')
for x in soup('meta',attrs = {'name':'title'}):
    f.write(4*' ' + x.get('content',None) + '\n')
#for x in soup('meta',attrs = {'name':'description'}):
#    print(x.get('content',None))
for x in soup('p',text = True):
    if len(remove_tags(str(x)).rstrip()) > 2:
        f.write(remove_tags(str(x)) + '\n\n')
f.close()
