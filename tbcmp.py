from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

f = open("1thucunimorphs.txt")

morphlemms = {}
morphlemms_perseus = {}
morphlemms_proiel = {}
pos_perseus = {}
morphpos = {}

hit = 0
hit2 = 0
hit3 = 0
fail = 0
for l in f:
 a = l.split('\t')
 if(len(a)<5):
  continue
 curcit = re.sub('([0-9]\.)[0]*([1-9][0-9]*\.[0-9]+)\-.+','\g<1>\g<2>',a[2])
 morphlemms[a[0] + '-' + curcit] = a[1]
 morphpos[a[0] + '-' + curcit] = a[4]

f.close()

fails = 0
hits = 0
f = open("thuc.tb.proiel.txt")
for l in f:
  m = re.search('^([0-9]\.[0-9]+\.[0-9]+)',l)
  if(m):
    curcit = m[1]
  m = re.search('"text": "([^"]+)',l)
  if(m):
   curform = m[1]
  m = re.search('"lemma": "([^"]+)',l)
  if(m):
   curlemma = m[1]
   fullcit = curform + '-' + curcit
   morphlemms_proiel[fullcit] = curlemma
f.close()

f = open("thuc.tb.perseus.txt")
for l in f:
  m = re.search('^([0-9]\.[0-9]+\.[0-9]+)',l)
  if(m):
    curcit = m[1]
  m = re.search('"text": "([^" ]+)',l)
  if(m):
   curform = m[1]
  m = re.search('"lemma": "([^" ]+)',l)
  if(m):
   curlemma = m[1]
   fullcit = curform + '-' + curcit
   morphlemms_perseus[fullcit] = curlemma
  m = re.search('"xpos": "([^" ]+)',l)
  if(m):
   curxpos = m[1]
   fullcit = curform + '-' + curcit
   pos_perseus[fullcit] = curxpos
f.close()

for foo in morphlemms:
  if( not foo in morphlemms_perseus):
    print(foo,"missing in perseus")
    perslem = 'noperslemm'
  else:
    perslem = morphlemms_perseus[foo]
  if( not foo in morphlemms_proiel):
    print(foo,"missing in proiel")
    proiellem = 'noproiellemm'
  else:
    proiellem = morphlemms_proiel[foo]

  #if( morphlemms[foo] ==  perslem):
    

  if( morphlemms[foo] ==  perslem and morphlemms[foo] == proiellem):
     hit = hit + 1
     continue
  if( morphlemms[foo] ==  perslem):
     hit2 = hit2 + 1
     continue
  if( morphlemms[foo] == proiellem):
     hit3 = hit3 + 1
     continue
  fail = fail + 1
  print("fail1",foo,morphlemms[foo], perslem,proiellem)

print(hit,hit2,hit3,fail)

