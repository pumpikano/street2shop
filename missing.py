import os

d = open('photos/photos.txt', 'r').readlines()
f = os.listdir('images/')

def split(x):
    first = x.find(',')
    return (x[:first], x[first+1:])

have = set([os.path.splitext(x)[0] for x in f])
urls = dict(map(lambda x: split(x.strip()), d))
diff = set(urls.keys()) - have

missing = dict(kv for kv in urls.iteritems() if kv[0] in diff)
open('missing','w').writelines([','.join(x) + '\n' for x in missing.iteritems()])
