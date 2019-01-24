import ast
import subprocess
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
    if choice == 'quit':
        quit()
    if choice in itemrange:
        print(matchdict[choice])
        print(dictionary[matchdict[choice]])
