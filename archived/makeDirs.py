import os
path_name = '{}/{}'.format(os.getcwd(),'happy')
if not os.path.exists(path_name):
    os.makedirs(path_name)
    print(path_name,'created.')
file_name = 'happyhappy'
with open('{}/{}.txt'.format(path_name,file_name),'w+') as f:
    f.write('very happy')
