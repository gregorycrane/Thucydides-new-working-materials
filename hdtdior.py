from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

lemcount = {}
inquote = 0

ids = []
form = {}
formb = {}
divclasses = {}
sentences = {}
entry = {}
lemma = {}
POS = {}
TTDis = {}
analysis = {}


f = open("herod-diorisis.xml","r")
i = 0
for l in f:
  if( re.search('id="([0-9]+)" location="([^"]+)',l)):
    m = re.search('id="([0-9]+)" location="([^"]+)',l)
    cursentence = m[1]
    curlocation = re.sub('\.[0-9a-zA-Z]+$','',m[2])
    #print(cursentence,curlocation)
  if( re.search('word form="([^"]+).*id="([0-9]+)',l)):
    m = re.search('word form="([^"]+).*id="([0-9]+)',l)
    curbeta = m[1]
    curbeta = re.sub("^'","",curbeta)
    curbeta = re.sub("'","ʼ",curbeta)
    curword = r.beta_code(curbeta)
    curwordid = curlocation + '@' + curword
    if( curwordid in divclasses):
      divclasses[curwordid] = divclasses[curwordid] + 1
    else:
      divclasses[curwordid] = 1
    fullwordid = curwordid + "[" + str(divclasses[curwordid]) + "]"
    sentences[fullwordid] =  cursentence
    form[fullwordid] = curword
    formb[fullwordid] = curbeta
    ids.append(fullwordid)
   # print(fullwordid)
  l = re.sub('(disambiguated="[^"]+") (TreeTagger="[^"]+")','\g<2> \g<1>',l)
  m = re.search('lemma id="([^"]+)" entry="([^"]+)" POS="([^"]+)" TreeTagger="([^"]+)" disambiguated="([^"]+)"',l)
  if(m):
    lemma[fullwordid] = m[1]
    #print(fullwordid,lemma[fullwordid])
    entry[fullwordid] = m[2]
    POS[fullwordid] = m[3]
    TTDis[fullwordid] = m[4] + "-" + m[5]
    #analysis[fullwordid] = 

  m = re.search('analysis morph="([^"]+)',l)
  if(m):
   if (fullwordid in analysis):
    analysis[fullwordid] = analysis[fullwordid] + "<NL>" + m[1] + "</NL>"
   else:
    analysis[fullwordid] =  "<NL>" + m[1] + "</NL>"
  # print("analysis",fullwordid,analysis[fullwordid])

for foo in ids:
  if( not foo in lemma):
    print(foo,form[foo],formb[foo],sentences[foo],'nolemma','noentry','nopos','nodis','noanalysis',sep="\t")
  else:
    print(foo,form[foo],formb[foo],sentences[foo],lemma[foo],entry[foo],POS[foo],TTDis[foo],analysis[foo],sep="\t") 
