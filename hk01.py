import re
import requests
import time
from bs4 import BeautifulSoup

#the following function will be used to remove html tags. This is only used when the wanted text is enclosed by two tags.
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

#writeArticle-----------------------------------------------------------------------------------------------------------------
def writetxt(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    #f = open('{}.txt'.format(soup('meta',attrs = {'name':'title'})[0].get('content',None),'w+'))
    filename = soup('meta',attrs = {'name':'title'})[0].get('content',None)
    f = open('{}.txt'.format(filename),'w+')
    #title
    for x in soup('meta',attrs = {'name':'title'}):
        f.write(x.get('content',None) + '\n')
    #date and time
    for x in soup('meta',attrs = {'property="article:published_time"'}):
        f.write(x.get('content',None) + '\n')
    #paragraphs
    for x in soup('p'):
        if remove_tags(str(x).rstrip()) != '登入 ' and remove_tags(str(x).rstrip()) != '登入 / 註冊':
            f.write(4*' ' + remove_tags(str(x)) + '\n\n')
    f.close()
    print('{} created.'.format(filename))

#main page-----------------------------------------------------------------------------------------------------------------
#make a dictionary to store all the urls on the main page.
urls1 = dict()

#requests the html of the main page.
html = requests.get('https://www.hk01.com/tag/8502').text
soup = BeautifulSoup(html,'html.parser')

#store all the urls with '/01觀點/' into the 'urls' dictionary.
#a dictionary is used because hk01.com has two urls on the main page for each article.
for x in soup('a'):
    if '/01觀點/' in x.get('href',None):
        urls1[x.get('href',None)] = urls1.get(x.get('href',None),1)

#Write articles into files.
for url in urls1:
    writetxt('https://www.hk01.com{}'.format(url))

#infiniteScroll------------------------------------------------------------------------------------------------------------
#the following function gets the url to more articles in the infinite scroll.
def firstOffset(soup):
    for text in soup('script',text=True):
        nextOffset = re.findall('''"nextOffset":([0-9]{2,})''',str(text))
        for firstOffsetValue in nextOffset:
            if firstOffsetValue != '[]':
                return firstOffsetValue

#this function is used for parsing the retrieved JSON from the infinite scroll.
def parseJSON(offsetValue):
    JSON = requests.get('https://web-data.api.hk01.com/v2/feed/tag/8502?offset={}&bucketId=00000'.format(offsetValue)).json()
    urls = list()
    for item in JSON['items']:
        urls.append(item['data']['canonicalUrl'])
    nextOffsetValue = JSON['nextOffset']
    return (urls,nextOffsetValue)

firstOffsetValue = firstOffset(soup)
(urls,nextOffsetValue) = parseJSON(firstOffsetValue)

count = 0
while True:
    for url in urls:
        writetxt(url)
    (urls,nextOffsetValue) = parseJSON(nextOffsetValue)
    count += 1
    if count > 1:
        break
