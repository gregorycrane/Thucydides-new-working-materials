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
 if( re.search('syntacticbreak',l)):
  hassubj = ''
  hasopt = ''

 a = l.split('\t')
 if(len(a)<5):
  continue
 curcit = re.sub('([0-9]\.)[0]*([1-9][0-9]*\.[0-9]+)\-.+','\g<1>\g<2>',a[2])
 morphlemms[a[0] + '-' + curcit] = a[1]
 morphpos[a[0] + '-' + curcit] = a[4]
 if( re.search(' subj',l)):
   hassubj = a[0]
   if( hasopt and hassubj):
    print(curcit,hassubj,hasopt)
 if( re.search(' opt',l)):
   hasopt = a[0]
   if( hasopt and hassubj):
    print(curcit,hassubj,hasopt)

f.close()

