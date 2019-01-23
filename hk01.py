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
                itemrange.append(str(x))
            break
        except:
            print('Input error')
            continue
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
            print('{} (y/n)?'.format(tag))
            yesno = input('input: ')
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
        return '{}'.format(dictionary[tag])

#getHref-----------------------------------------------------------------------------------------------------------------
def getHref(taginp):
    pattern = re.compile(r'^/[0-9]*[\u4e00-\u9fff]+')
    for tag in taginp.split(','): #some pages have more than one tag
        urls = list()
        html = requests.get('https://www.hk01.com/tag/{}'.format(tag)).text
        soup = BeautifulSoup(html,'html.parser')
        #print(re.findall(r'''"canonicalUrl":"(.+?)"''',html))
        for tag in soup('a'):
        #    print(tag.get('href'))
            if tag.get('href',None) != None:
                if re.match(pattern,tag.get('href')):
                    if 'https://www.hk01.com/{}'.format(tag.get('href')) not in urls:
                        urls.append('https://www.hk01.com/{}'.format(tag.get('href')))
    return urls        #return urls, which is a list of urls found on the main page

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
    print('{} created.'.format(filename))
    nextstep = input('''Press 'Enter' to continue, type 'quit' to exit: ''')
    if nextstep == 'quit':
        quit()

#the following function will be used to remove html tags. This is only used when the wanted text is enclosed by two tags.
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def main():
    tag = directory()
    urls = getHref(tag)
    for url in urls:
        print(url)
        writetxt(url)

#__main__
if __name__ == '__main__':
    main()
