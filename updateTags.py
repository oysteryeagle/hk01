def updateTags():
    #scrape tags
    import scrapy

    #sort tags
    import ast
    with open('tags.json') as f:
        lis = ast.literal_eval(f.read())
        lis = sorted(lis, key = lambda i: i['tagNumber'])
    with open('tags.txt','w') as f:
        f.write(str(lis))

if __name__ == '__main__':
    updateTags()
