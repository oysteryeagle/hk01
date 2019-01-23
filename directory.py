import ast
import time
import subprocess

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
    print('tag: {}'.format(dictionary[tag]))
