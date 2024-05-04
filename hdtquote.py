from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

lemcount = {}
inquote = 0

f = open("tlg0016.tlg001.perseus-grc2.xml","r")
for l in f:
  if( inquote ):
    if(re.search('^([^”]+)”',l)):
     l = re.sub('^([^”]+)”','<q type="direct" rend="merge">\g<1></q>',l)
     inquote = 0
    else:
     if( not re.search('^[ \t]*<',l)):
      l = re.sub('^(.+)','<q type="direct" rend="merge">\g<1></q>',l)
  while(re.search('“([^”]+)”',l)):
   l = re.sub('“([^”]+)”','<q type="direct">\g<1></q>',l)
  if( re.search('“([^”]+)$',l)):
   inquote = 1
   l = re.sub('“([^”]+)$','<q type="direct">\g<1></q>',l)
  l = re.sub('(<q[^>]*>)','\n\g<1>\n',l)
  l = re.sub('(<\/q>|<\/quote>)','\n\g<1>\n',l)
  print(l,end='')
 

