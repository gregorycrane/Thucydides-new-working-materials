from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

lemcount = {}
inquote = 0

f = open("herod-diorisis.xml","r")
for l in f:
  if( re.search('id="([0-9]+)" location="([^"]+)',l)):
    m = re.search('id="([0-9]+)" location="([^"]+)',l)
    cursentence = m[1]
    curlocation = m[2]
    print(cursentence,curlocation)
  if( re.search('word form="([^"]+).*id="([0-9]+)',l)):
    m = re.search('word form="([^"]+).*id="([0-9]+)',l)
    curword = r.beta_code(m[1])
    curid = m[2]
    print(curword,curid)
