from cltk.corpus.greek.beta_to_unicode import Replacer
import re

r = Replacer()

curchap = 0
curbook = 0
cursect = 0
f = open("ToposTextThucycides.html","r")
curcit = ''
for l in f:
  m = re.search(r'urn:cts:greekLit:tlg0003.tlg001:([0-9]+\.[0-9]+)',l)
  if(m):
   curcit = m.group(1)
  if( not m):
   continue
#get places with long/lat coordinates
  while(re.search(r'https:\/\/topostext.org\/([^\/]+)\/([^"]+)[^>]+>([^<]+)',l)):
    m = re.search(r'https:\/\/topostext.org\/([^\/]+)\/([^"]+)([^>]+>)([^<]+)',l)
    curtype = m.group(1)
    curid = m.group(2)
    n = re.search('.+(long="[0-9\.]+" lat="[0-9\.]+)',m.group(3))
    if( n ):
      lonlat = ' ' + n.group(1)
    else:
      lonlat = ''
    curstring = m.group(4)
    n = re.search(r'class="([^" ]+)',m.group(3))
    if(n):
      curclass = n.group(1)
    else:
      curclass = "noclass"
    print(curcit,curtype,curid,curclass,curstring,lonlat)
    l = re.sub(r'https:\/\/topostext.org\/([^\/]+)\/([^"]+)[^>]+>([^<]+)',' ',l,1)
 
