import requests
from bs4 import BeautifulSoup

with open('tags.txt','a+') as f:
    for index in range(9998,10000):
        response = requests.get('https://www.hk01.com/tag/{}'.format(index))
        if response.status_code != 200: #could also check == requests.codes.ok
            continue
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        title = soup('meta',attrs = {'name':'title'})[0].get('content',None).split('｜')[0]
        f.write('{} {}\n'.format(index,title))
        print(index,title)
