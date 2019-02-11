import requests

html = requests.get('https://www.hk01.com/社會新聞/286495/小巴駕駛執照持有人年紀老化-近四成年過60歲-創5年新高').text
with open('html2.txt','w+') as f:
    f.write(html)
