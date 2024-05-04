from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

lemcount = {}
inquote = 0

trainf = open("thhdt-trainn.txt","w")
testf = open("thhdt-testn.txt","w")
outf = trainf

i = 0
f = open("thucunimorphs.txt")
for l in f:
  if(re.search('syntacticbreak',l)):
    i = i +1
    if( i < 101):
      outf = testf
    else:
      print('',file=outf)
      outf = trainf

    print('',file=outf)
    print("__label__thuc__",file=outf,end=" ")

  a = l.split('\t')
  if(len(a) < 5):
    continue
  if( a[4].islower()):
   print(a[4],file=outf,end=' ')
  else:
   print('name',file=outf,end=' ')
f.close()
print('',file=outf)

i = 0
f = open("herod-diorisis.xml")
outf = testf
for l in f:
  if(re.search('<sentence',l)):
   print('',file=outf)
   print("__label__hdt__",file=outf,end=" ")
   i = i +1
   if( i < 101):
      outf = testf
   else:
      outf = trainf
  m = re.search('entry="([^"]+)',l)
  if(m):
   if(m[1].islower()):
    print(m[1],file=outf,end=" ")
   else:
    print('name',file=outf,end=" ")
print('',file=outf)
f.close()
