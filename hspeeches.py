from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

conjforms = {}
formcount = {}
formcountbk2 = {}

lemcount = {}
lemcountbk2 = {}
lemdefs = {}

pparts = {}
ppartsbk2 = {}
inspeech = {}
forms = {}

formquizbk2 = {}

lexicalentries = {}
lexfile = "GreekMorphApril18.csv"
with open(lexfile) as f:
    for line in f:

        #print(line)
        #line = line.strip('"')
        fields = line.split(",")
        fields[1] = fields[1].strip('"')
        fields[2] = fields[2].strip('\n')
        fields[2] = fields[2].strip('"')
        lexicalentries[fields[1]] = fields[2]

f.close()

narrwords = 0
quotewords = 0
narrlist = {}
quotelist = {}
fulwords = {}
fulllist = {}
fullwords = 0
pos = {}
f = open("hdt-q.txt","r")
for l in f:
  a = l.split('\t')
  if( re.search('(narrative|inquote)',l)):
    fullwords = fullwords + 1
    curlemma = a[3]
    pos[curlemma] = a[4]
    if( curlemma in fulllist):
       fulllist[curlemma] = fulllist[curlemma] + 1
    else:
       fulllist[curlemma] = 1
  if( re.search('narrative',l)):
    narrwords = narrwords + 1
    curlemma = a[3]
    pos[curlemma] = a[4]
    if( curlemma in narrlist):
       narrlist[curlemma] = narrlist[curlemma] + 1
    else:
       narrlist[curlemma] = 1
  if( re.search('inquote',l)):
    quotewords = quotewords + 1
    curlemma = a[3]
    if( curlemma in quotelist):
       quotelist[curlemma] = quotelist[curlemma] + 1
    else:
       quotelist[curlemma] = 1


for foo in fulllist:
   avg1 = (10000*fulllist[foo])/fullwords
   if( foo in quotelist):
      tot2 = quotelist[foo]
      avg2 = (10000*quotelist[foo])/quotewords
   else:
      tot2 = 0
      avg2 = 0
   if( foo in narrlist):
      tot3 = narrlist[foo]
      avg3 = (10000*narrlist[foo])/narrwords
   else:
      tot3 = 0
      avg3 = 0

   if( avg2 ):
      avg4 = avg3/avg2
      avg4 = re.sub('(\.[0-9][0-9]).*','\g<1>',str(avg4))
   else:
      avg4 = 1000

   avg1 = re.sub('(\.[0-9][0-9]).*','\g<1>',str(avg1))
   avg2 = re.sub('(\.[0-9][0-9]).*','\g<1>',str(avg2))
   avg3 = re.sub('(\.[0-9][0-9]).*','\g<1>',str(avg3))

   if(fulllist[foo] > 9):
     if( foo in lexicalentries):
      shortdef = lexicalentries[foo]
     else:
      shortdef = 'nodef'
     print(avg4,foo,pos[foo],'tot',fulllist[foo],avg1,'q',tot2,avg2,'n',tot3,avg3,shortdef,sep="\t")
