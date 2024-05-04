from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

lemcount = {}
inquote = 0

curbook = 0
curchapter = 0
cursection = 0

ids = {}
sentences = {}
form = {}
entry = {}
lemma = {}
POS = {}
TTDis = {}
analysis = {}

f = open("hdt-dior.txt","r")
for l in f:
  l = re.sub('\n$','',l)
  args = l.split('\t')
  curid = args[0]
  curid2 = re.sub('\.[0-9a]+$','',curid)
  ids[curid] = 1
  curform = args[1]
  form[curid] = curform
  sentences[curid] = args[3]
  entry[curid] = args[5]
  entry[curform] = args[5]
  POS[curid] = args[6]
  POS[curform] = args[6]
  analysis[curid] = args[8]
  analysis[curform] = args[8]


f.close()

divclasses = {}
f = open("tlg0016.tlg001.perseus-grc2.xml","r")
for l in f:
 if(re.search('<q[^u]',l) ):
   inquote = inquote + 1
 if(re.search('<\/q>',l) ):
   inquote = inquote - 1
 m = re.search(' subtype="book" n="([^"]+)',l)
 if(m):
   curbook = m[1]
 m = re.search(' subtype="chapter" n="([^"]+)',l)
 if(m):
   curchapter = m[1]
 m = re.search(' subtype="section" n="([^"]+)',l)
 if(m):
   cursection = m[1]
 l = re.sub('[a-zA-Z0-9]+',' ',l)
 wtxt = re.sub('<note[^>]*>[^<]+</note>',' ' ,l)
 wtxt = re.sub('<[^>]+>',' ' ,wtxt)
 words = wtxt.split()
 if(cursection == 0):
  continue
 curref = str(curbook) + '.' + str(curchapter) + '.'+ str(cursection)
 curref2 = str(curbook) + '.' + str(curchapter) 
 for foo in words:
   foo = re.sub('[-·\s,\.;;()]','',foo)
   if(re.search('^[0-9]+$',foo) or foo == ''):
    continue

   curwordid = curref + '@' + foo
   if( curwordid in divclasses):
      divclasses[curwordid] = divclasses[curwordid] + 1
   else:
      divclasses[curwordid] = 1
   fullwordid = curwordid + "[" + str(divclasses[curwordid]) + "]"

   curwordid2 = curref2 + '@' + foo
   if( curwordid2 in divclasses):
      divclasses[curwordid2] = divclasses[curwordid2] + 1
   else:
      divclasses[curwordid2] = 1
   fullwordid2 = curwordid2 + "[" + str(divclasses[curwordid2]) + "]"

   if(inquote):
    inq = 'inquote' + str(inquote)
   else:
    inq = 'narrative' + str(inquote)
   useid = fullwordid2
   if( fullwordid2 not in ids):
     if( foo in entry ):
    #   print("backupid",foo)
       useid = foo
     else:
       print("no entry",fullwordid2)
       continue

   print(foo,fullwordid,curref,entry[useid],POS[useid],inq,analysis[useid],sep='\t')
