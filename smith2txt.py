from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re


r = Replacer()

f = open("smith.thuc.index.xml","r")
curtype = 'notype'
curname = ''
curid = ''
cursubhead = ''
curhead = ''
for l in f:
  m = re.search('"([^\"]+)(-smthuc-[0-9]+)',l)
  if(m):
   curname = re.sub('\-',' ',m.group(1))
   curid = m.group(1) + m.group(2)
   #print(curname,curid,sep="\t")
   curtype = 'notype'
  if( re.search('<head><placeName',l)):
    curtype = 'place'
  if( re.search('<head><pers',l)):
    curtype = 'person'
  if( re.search('<head><name type="ethnic',l)):
    curtype = 'ethnic'
  if( re.search('<orgName',l)):
    curtype = 'organization'
  if( re.search('<head>(.+)<.head>',l)):
    m = re.search('<head>(.+)<.head>',l)
    if( re.search('<div type="subentry',l)):
      curhead = m.group(1)
      cursubhead = ''
    else:
      cursubhead = m.group(1)
  while( re.search(r'"(Thuc[^"]+)',l)):
   m = re.search(r'"(Thuc[^"]+)',l)
   curcit = m.group(1)
   print(curcit,curtype,curname,curid,curhead,cursubhead,sep="\t")
   l = re.sub(r'"(Thuc[^"]+)','',l,1)
