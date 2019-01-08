import requests

html = requests.get('https://www.hk01.com/01觀點/182819/01周報社論-發展高球場非仇商-社會整體利益為重').text
f = open('html2.txt','w+')
f.write(html)
f.close()
