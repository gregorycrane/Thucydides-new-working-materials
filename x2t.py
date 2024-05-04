from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

lemcount = {}
inquote = 0

f = open(
def dotext(name):
 f = open(name,"r")
 for l in f:
  a = l.split('\t')
  print(a[5])

 return
 intext = 0
 for l in f:
  if( re.search('<body',l)):
   intext = 1
  if( not intext ):
   continue
  l = re.sub('<note[^>]*>[^<]+',' ',l)
  l = re.sub('[-·,\.;;()]','',l)
  l = re.sub('<[^>]+>',' ',l)
  print(l,end='')
 f.close()

dotext("hdt-dior.txt")
dotext("tlg0016.tlg001.perseus-grc2.xml")
