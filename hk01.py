print('initializing...')
import requests
import re
import ast
import subprocess
import time
import os
from bs4 import BeautifulSoup
#directory-----------------------------------------------------------------------------------------------------------------
def directory():
    itemrange = list()
    subprocess.run('clear')
    print('香港01新聞下載器')
    #initial setup
    print('Number of topics per page: ')
    while 1:
        #num = input()
        try:
            num = 10#int(num)
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
    print(20*'-'+f'page {page}')
    #------------------------------------------------------------------------------------
    while 1:
        nextstep = input('f/b: ')
        if nextstep == 'quit':
            quit()
        elif nextstep in itemrange:
            tag = list(dictionary)[start+int(nextstep)-1]
            print(f'{tag} (y/n)? ',end='')
            yesno = input()
            if yesno == 'n':
                continue
            elif yesno == 'y':
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
            print(20*'-'+f'page {page}')
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
            print(20*'-'+f'page {page}')
            #------------------------------------------------------------------------------------
    print(f'fetching {tag}...')
    with open('dictionary.txt') as f:
        dictionary = ast.literal_eval(f.read())
        return f'{dictionary[tag]}',tag #returns the tag number corresponding to the tag name

#search-----------------------------------------------------------------------------------------------------------------
def search():
    matchlist = list() #list the match items
    matchdict = dict() #link the entry number with the tag number
    itemrange = list()
    subprocess.run('clear')
    print('香港01新聞下載器')
    with open('dictionary.txt','r') as f:
        dictionary = ast.literal_eval(f.read())
        while 1:
            find = input('search: ')
            if find == 'quit':quit()
            for item in dictionary:
                if find in item:
                    matchlist.append(item)
            if len(matchlist)>0:break
            else: print(f'{find} not found')
    for index,item in enumerate(matchlist):
        print(index+1,item)
        itemrange.append(str(index+1)) #user input is string so range must also be string
        matchdict[str(index+1)] = item
    while 1:
        choice = input('item number: ')
        if choice == 'quit': quit()
        elif choice in itemrange:
            yesno = input(f'{matchdict[choice]}? (y/n/quit)')
            if yesno == 'quit': quit()
            elif yesno == 'n': continue
            elif yesno == 'y':
                tagnum = dictionary[matchdict[choice]]
                tag = matchlist[int(choice)-1]
                return tagnum,tag

#getHref-----------------------------------------------------------------------------------------------------------------
def getHref(taginp):
    pattern = re.compile(r'^/[0-9]*[\u4e00-\u9fff]+')
    for tag in taginp.split(','): #some pages have more than one tag
        urls = list()
        html = requests.get(f'https://www.hk01.com/tag/{tag}').text #requests html of the main page
        soup = BeautifulSoup(html,'html.parser')
        #print(re.findall(r'''"canonicalUrl":"(.+?)"''',html))
        for tag in soup('a'): #finding all the anchor tags and extracting the urls that contains chinese characters
            if 'https://www.hk01.com/{}'.format(tag.get('href')) not in urls and re.match(pattern,tag.get('href')):
                urls.append('https://www.hk01.com/{}'.format(tag.get('href')))
    return urls,soup       #return urls, which is a list of urls found on the main page. Returns soup of the main page for getting firstOffset value later.

#infiniteScroll------------------------------------------------------------------------------------------------------------
#the following function gets the url to more articles in the infinite scroll.
def firstOffset(soup):
    for text in soup('script',text=True):
        nextOffset = re.findall('''"nextOffset":([0-9]{2,})''',str(text))
        for firstOffsetValue in nextOffset:
            if firstOffsetValue != '[]':
                #print(firstOffsetValue)
                return firstOffsetValue

#this function is used for parsing the retrieved JSON from the infinite scroll.    ERRRROROROROR
def parseJSON(tag,offsetValue):
    JSON = requests.get('https://web-data.api.hk01.com/v2/feed/tag/{}?offset={}&bucketId=00000'.format(tag,offsetValue)).json()
    urls = list()
    for item in JSON['items']:
        urls.append(item['data']['canonicalUrl'])
    try:
        nextOffsetValue = JSON['nextOffset']
    except:
        return (urls,None)
    return (urls,nextOffsetValue)

#makeDirs---------------------------------------------------------------------------------------------------------------------
def makeDirs(tag):
    pass
    path_name = f'{os.getcwd()}/{tag}'
    if not os.path.exists(path_name):
        os.makedirs(path_name)
        print('folder created:',path_name)
    return path_name
#writeArticle-----------------------------------------------------------------------------------------------------------------
def writetxt(url,tag):
    path_name = makeDirs(tag)
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    #date and time
    for x in soup('meta',attrs = {'property':'article:published_time'}):
            time = x.get('content').split('T')[0]
    #f = open(f'{soup('meta',attrs = {'name':'title'})[0].get('content',None)}.txt','w+'))
    filename = soup('meta',attrs = {'name':'title'})[0].get('content',None) + f'--{time}'
    with open(f'{path_name}/{filename}.txt','w+') as f:
    #title
        for x in soup('meta',attrs = {'name':'title'}):
            f.write(x.get('content',None) + '\n')
        #write date and time
        f.write(f'{time}\n')
        #paragraphs
        for x in soup('p'):
            if remove_tags(str(x).rstrip()) != '登入 ' and remove_tags(str(x).rstrip()) != '登入 / 註冊':
                f.write(4*' ' + remove_tags(str(x)) + '\n\n')
    print(f'{filename} created at:\n{path_name}')

#the following function will be used to remove html tags. This is only used when the wanted text is enclosed by two tags.
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)
#menu(url)
def menu(urls,tag,nextOffsetValue):
    dlmenu = dict()
    itemrange = list()
    for index,url in enumerate(urls,1):
        dlmenu[index] = url
        itemrange.append(str(index))
        print(index,url)
    while 1:
        choice = input('(f/quit): ')
        if choice in itemrange:
            print(f'{dlmenu[int(choice)]} (y/n)? ',end='')
            yesno = input('(y/n/quit)')
            if yesno == 'n':
                continue
            elif yesno == 'y':
                writetxt(dlmenu[int(choice)],tag)
        elif choice == 'f':
            if nextOffsetValue == None:
                print('No more article found.')
                continue
            break
        elif choice == 'quit':
            quit()
#main()
def main():
    nextOffsetValue = -1
    subprocess.run('clear')
    print('香港01新聞下載器')
    while 1:
        mode = input('mode (directory/search): ')
        if mode == 'directory':
            tagnum,tag = directory()
            print('setting up...')
            break
        elif mode == 'search':
            tagnum,tag = search()
            print('setting up...')
            break
        elif mode == 'quit':
            quit()
    urls,soup = getHref(tagnum)
    subprocess.run('clear')
    menu(urls,tag,nextOffsetValue)
    #get the offset value from the main page.
    print('''retrieving more items...''')
    firstOffsetValue = firstOffset(soup)
    (urls,nextOffsetValue) = parseJSON(tagnum,firstOffsetValue)
    #use the old offset value to find the new offset value and urls of articles. Repeats until no more offset value is found.
    while 1:
        menu(urls,tag,nextOffsetValue)
        print('''retrieving more items...''')
        (urls,nextOffsetValue) = parseJSON(tagnum,nextOffsetValue)
        subprocess.run('clear')
#__main__
if __name__ == '__main__':
    main()
