import ast
import time

t0 = time.time()
with open('dictionary.txt') as f:
    dictionary = ast.literal_eval(f.read())
#print(dictionary)
print(time.time()-t0)
