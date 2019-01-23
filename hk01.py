import requests
from bs4 import BeautifulSoup
import re
import ast
import subprocess

#directory-----------------------------------------------------------------------------------------------------------------
def directory():
    itemrange = list()
    subprocess.run('clear')
    print('香港01新聞下載器')
    #initial setup
    print('Number of topics per page: ')
    while 1:
        num = input()
        try:
            num = int(num)
            for x in range(1,num+1):
                itemrange.append(str(x)) #create a list that validates user input
            break
        except:
            print('Input error')
    start = 0
    end = len(itemrange)
    itemsperpage = len(itemrange)
    page = 1

    with open('dictionary.txt') as f:
        dictionary = ast.literal_eval(f.read())
    #menu
    #display-----------------------------------------------------------------------------
    subprocess.run('clear')
    print('香港01新聞下載器')
    print(20*'-')
    for index,topic in enumerate(list(dictionary)[start:end],1):
        print(index,topic)
    print(20*'-'+'page {}'.format(page))
    #------------------------------------------------------------------------------------
    while 1:
        nextstep = input('f/b: ')
        if nextstep == 'quit':
            quit()
        elif nextstep in itemrange:
            tag = list(dictionary)[start+int(nextstep)-1]
            print('{} (y/n)? '.format(tag),end='')
            yesno = input()
            if yesno == 'n':
                continue
            if yesno == 'y':
                break
        elif nextstep == 'f': #next page (forward)
            start += itemsperpage
            end += itemsperpage
            page += 1
            #display-----------------------------------------------------------------------------
            subprocess.run('clear')
            print('香港01新聞下載器')
            print(20*'-')
            for index,topic in enumerate(list(dictionary)[start:end],1):
                print(index,topic)
            print(20*'-'+'page {}'.format(page))
            #------------------------------------------------------------------------------------
        elif nextstep == 'b': #previous page (back)
            start -= itemsperpage
            end -= itemsperpage
            page -= 1
            #display-----------------------------------------------------------------------------
            subprocess.run('clear')
            print('香港01新聞下載器')
            print(20*'-')
            for index,topic in enumerate(list(dictionary)[start:end],1):
                print(index,topic)
            print(20*'-'+'page {}'.format(page))
            #------------------------------------------------------------------------------------
    print('fetching {}...'.format(tag))
    with open('dictionary.txt') as f:
        dictionary = ast.literal_eval(f.read())
        return '{}'.format(dictionary[tag]) #returns the tag number corresponding to the tag name

#search-----------------------------------------------------------------------------------------------------------------
def search():
    subprocess.run('clear')
    matchlist = list()
    matchdict = dict()
    itemrange = list()
    with open('dictionary.txt','r') as f:
        dictionary = ast.literal_eval(f.read())
        find = input('find: ')
        for item in dictionary:
            if find in item:
                matchlist.append(item)
    for index,item in enumerate(matchlist):
        print(index+1,item)
        itemrange.append(str(index+1)) #user input is string so range must also be string
        matchdict[str(index+1)] = item
    while 1:
        choice = input()
        if choice in itemrange:
            yesno = input('{}? (y/n/quit)'.format(matchdict[choice]))
            if yesno == 'quit': quit()
            if yesno == 'n': continue
            if yesno == 'y':
                tag = dictionary[matchdict[choice]]
                return tag

#getHref-----------------------------------------------------------------------------------------------------------------
def getHref(taginp):
    pattern = re.compile(r'^/[0-9]*[\u4e00-\u9fff]+')
    for tag in taginp.split(','): #some pages have more than one tag
        urls = list()
        html = requests.get('https://www.hk01.com/tag/{}'.format(tag)).text #requests html of the main page
        soup = BeautifulSoup(html,'html.parser')
        #print(re.findall(r'''"canonicalUrl":"(.+?)"''',html))
        for tag in soup('a'): #finding all the anchor tags and extracting the urls that contains chinese characters
            if tag.get('href',None) != None:
                if re.match(pattern,tag.get('href')):
                    if 'https://www.hk01.com/{}'.format(tag.get('href')) not in urls:
                        urls.append('https://www.hk01.com/{}'.format(tag.get('href')))
    return urls,soup       #return urls, which is a list of urls found on the main page. Returns soup of the main page for getting firstOffset value later.

#infiniteScroll------------------------------------------------------------------------------------------------------------
#the following function gets the url to more articles in the infinite scroll.
def firstOffset(soup):
    for text in soup('script',text=True):
        nextOffset = re.findall('''"nextOffset":([0-9]{2,})''',str(text))
        for firstOffsetValue in nextOffset:
            if firstOffsetValue != '[]':
                return firstOffsetValue

#this function is used for parsing the retrieved JSON from the infinite scroll.
def parseJSON(tag,offsetValue):
    JSON = requests.get('https://web-data.api.hk01.com/v2/feed/tag/{}?offset={}&bucketId=00000'.format(tag,offsetValue)).json()
    urls = list()
    for item in JSON['items']:
        urls.append(item['data']['canonicalUrl'])
    try:nextOffsetValue = JSON['nextOffset']
    except:
        print('No more article found.')
        input('Press Enter to quit.')
        quit()
    return (urls,nextOffsetValue)

#writeArticle-----------------------------------------------------------------------------------------------------------------
def writetxt(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    #date and time
    for x in soup('meta',attrs = {'property':'article:published_time'}):
            time = x.get('content').split('T')[0]
    #f = open('{}.txt'.format(soup('meta',attrs = {'name':'title'})[0].get('content',None),'w+'))
    filename = soup('meta',attrs = {'name':'title'})[0].get('content',None) + '--{}'.format(time)
    f = open('{}.txt'.format(filename),'w+')
    #title
    for x in soup('meta',attrs = {'name':'title'}):
        f.write(x.get('content',None) + '\n')
    #write date and time
    f.write('{}\n'.format(time))
    #paragraphs
    for x in soup('p'):
        if remove_tags(str(x).rstrip()) != '登入 ' and remove_tags(str(x).rstrip()) != '登入 / 註冊':
            f.write(4*' ' + remove_tags(str(x)) + '\n\n')
    f.close()
    print('{} created.\n'.format(filename))

#the following function will be used to remove html tags. This is only used when the wanted text is enclosed by two tags.
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def main():
    while 1:
        mode = input('mode (directory/search): ')
        if mode == 'directory':
            tag = directory()
            break
        if mode == 'search':
            tag = search()
            break
        if mode == 'quit':
            quit()
    urls,soup = getHref(tag)
    subprocess.run('clear')
    for url in urls:
        print('{} (y/n/quit): '.format(url),end='')
        while 1:
            writeyesno = input()
            if writeyesno == 'y':
                writetxt(url)
                break
            elif writeyesno == 'n':
                break
            elif writeyesno == 'quit':
                quit()
    #get the offset value from the main page.
    firstOffsetValue = firstOffset(soup)
    (urls,nextOffsetValue) = parseJSON(tag,firstOffsetValue)
    #use the old offset value to find the new offset value and urls of articles. Repeats until no more offset value is found.
    while 1:
        for url in urls:
            print('{} (y/n/quit): '.format(url),end='')
            while 1:
                writeyesno = input()
                if writeyesno == 'y':
                    writetxt(url)
                    break
                elif writeyesno == 'n':
                    break
                elif writeyesno == 'quit':
                    quit()
        (urls,nextOffsetValue) = parseJSON(tag,nextOffsetValue)

#__main__
if __name__ == '__main__':
    main()
