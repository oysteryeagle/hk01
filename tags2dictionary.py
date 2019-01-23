import time
import re
import json

dictionary = dict()
t0 = time.time()
with open('tags.txt') as f:
    tags = list(f)
    for  index,item in enumerate(tags):
        tags[index] = tags[index].replace('\n','')
        tag = tags[index].split(' ',1)
        if dictionary.get(tag[1],None) != None:
            dictionary[tag[1]] = dictionary.get(tag[1],None) + ',{}'.format(tag[0])
            continue
        dictionary[tag[1]] = tag[0]
        #print(tag[0])
        #time.sleep(0.01)
#print(dictionary)
print(time.time() - t0)
#try: print(dictionary[''])
#except: print()
with open('dictionary.txt','w+') as file:
    file.write(str(dictionary))
