from cltk.corpus.greek.beta_to_unicode import Replacer
import re

r = Replacer()
lem = r.beta_code('a)/ndra')

id2head = {}
curid = ''
curhead = ''
curbasename = ''
greeklabel = ''

def dofile(fname):
 id2head = {}
 curid = ''
 curhead = ''
 curbasename = ''
 greeklabel = ''

#f = open("viaf88890045.003.perseus-eng1.xml","r")
#f = open("../002/viaf88890045.002.xml","r")
 f = open(fname,"r")
 for l in f:
  m = re.search(r'xml:id="([^"]+)(-[gb][ei]o[\-0-9]*)"',l)
  if(m):
   curid = m.group(1) + m.group(2)
   curbasename = m.group(1).capitalize()
   curbasename = re.sub('-.+','',curbasename)
   greeklabel = ''
   print("#",curid)
  #if(m):
  # id2head[curbasename] = m.group(1)
  m = re.search(r'<persName xml:lang="grc"><surname[^>]*>([^<]+)',l)
  if(m):
   if( re.search('002.xml',fname) ):
    id2head[curbasename] = r.beta_code(m.group(1))
   else:
    id2head[curbasename] = m.group(1)
  m = re.search(r'<label\s+xml:lang="g[^>]+>([^<]+)',l)
  if(m):
   if( re.search('002.xml',fname) ):
    id2head[curbasename] = r.beta_code(m.group(1))
   else:
    id2head[curbasename] = m.group(1)
  if( not curbasename in id2head and re.search(r'<foreign xml:lang="grc">([^<,]+)',l)):
   m = re.search(r'<foreign xml:lang="grc">([^<,]+)',l)
   if( re.search('002.xml',fname) ):
    id2head[curbasename] = r.beta_code(m.group(1))
   else:
    id2head[curbasename] = m.group(1)
  while( re.search(r'<bibl n="([^"]+)',l)):
   m = re.search(r'<bibl n="([^"]+)',l)
   l =  re.sub(r'<bibl n="([^"]+)','',l,1)
   if(m):
    curcit = m.group(1)
    if( curbasename in id2head):
     print(curcit,curid,curbasename,curhead,id2head[curbasename])
    else:
     print(curcit,curid,curbasename,curhead,'nohead')
 f.close()

dofile("../canonical-pdlrefwk/data/viaf88890045/002/viaf88890045.002.xml")
dofile("../canonical-pdlrefwk/data/viaf88890045/003/viaf88890045.003.perseus-eng1.xml")
