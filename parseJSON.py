import requests
import re

#def parseJSON(offsetValue):
JSON = requests.get('https://web-data.api.hk01.com/v2/feed/tag/8502?offset=1540764000&bucketId=00000').json()
#JSON = requests.get('https://web-data.api.hk01.com/v2/feed/tag/8502?offset={}&bucketId=00000'.format(offsetValue)).json()
urls = list()
for item in JSON['items']:
#    print(item['data']['canonicalUrl'])
    urls.append(item['data']['canonicalUrl'])
#url = JSON['items'][0]['data']['canonicalUrl']
nextOffset = JSON['nextOffset']
print(urls)


#https://web-data.api.hk01.com/v2/feed/tag/8502?offset=1540764000&bucketId=00000
#https://web-data.api.hk01.com/v2/feed/tag/8502?offset=1534716000&bucketId=00000
#https://web-data.api.hk01.com/v2/feed/tag/8502?offset=1529877600&bucketId=00000
#nextOffset at the end of each JSON
