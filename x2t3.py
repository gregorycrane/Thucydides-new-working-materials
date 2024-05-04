from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

lemcount = {}
inquote = 0

trainf = open("thhdt-train.txt","w")
testf = open("thhdt-test.txt","w")
outf = trainf

i = 0
f = open("hdt-q.txt")
lastcit = ''
for l in f:
  if( re.search('no entry',l)):
    continue
  a = l.split('\t')
  curcit = a[2] + '-' + a[5]
  curlabel = re.sub('[\-0-9]+$','',a[5])
  curlabel = '__label__' + curlabel + '__'
  if( not curcit == lastcit):
    print('')
    print(curlabel,end=" ")
    lastcit = curcit
  print(a[3],end=" ")
  continue
 
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
  print(a[4],file=outf,end=' ')
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
   print(m[1],file=outf,end=" ")
print('',file=outf)
f.close()
