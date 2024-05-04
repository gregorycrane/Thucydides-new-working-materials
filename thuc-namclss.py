from cltk.corpus.greek.beta_to_unicode import Replacer
import re

r = Replacer()

curchap = 0
curbook = 0
cursect = 0
f = open("thuc.hist_gk.xml","r")
for l in f:
  m = re.search(r'n="([0-9]+)" type="book',l)
  if(m):
   curbook = m.group(1)
   curchapter = 0
   cursect = 0
   #print(curbook,curchap,cursect)
  m = re.search(r'chapter" n="([0-9]+)',l)
  if(m):
   curchap = m.group(1)
   cursect = 0
   #print(curbook,curchap,cursect)
  m = re.search(r'section" n="([0-9]+)',l)
  if(m):
   cursect = m.group(1)
   curcit = curbook + "." + curchap + "." + cursect
   #print(curcit)
  while( re.search('<(placeName|persName|name type="[^"]+")[ ]*key="[0-9]+:([^:]+):([^:]+):([^\t "]+)[^>]*>([^<]+)',l)):
    #print('line now',l)
    m = re.search('<(placeName|persName|name type="[^"]+")[ ]*key="[0-9]+:([^:]+):([^:]+):([^\t "]+)[^>]*>([^<]+)',l)
    if(m):
     curentity = r.beta_code(m.group(2))
     curtype = m.group(3)
     curmorph = m.group(4)
     curstring = r.beta_code(m.group(5))
     print(curcit,curtype,curentity,curstring,curmorph,sep="\t")
     l = re.sub('<(placeName|persName|name type="[^"]+")[ ]*key="[0-9]+:([^:]+):([^:]+):([^\t "]+)[^>]*>([^<]+)','',l,1)
