import ast
import time


start = 0
end = 10
page = 1
while True:
    with open('dictionary.txt') as f:
        dictionary = ast.literal_eval(f.read())
    print(20*'-')
    for index,topic in enumerate(list(dictionary)[start:end],1):
        print(index,topic)
    print(20*'-'+'page {}'.format(page))
    nextstep = input('f/b: ')
    if nextstep == 'quit':
        quit()
    elif nextstep == 'f':
        start += 10
        end += 10
        page += 1
    elif nextstep == 'b':
        start -= 10
        end -= 10
        page -= 1
