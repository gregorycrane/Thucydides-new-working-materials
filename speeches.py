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

f = open("thuc-speeches.txt","r")
for l in f:
   m = re.search('([1-8])\.([0-9]+)\-[1-8]\.([0-9]+)',l)
   if(m):
     book = m[1]
     start = m[2]
     stop = m[3]
     if( int(stop) < int(start) ):
       print("error",stop,"less than", start,l)
     for x in range(int(start),int(stop)):
       inspeech[str(book)+"."+str(x)] = 1
     inspeech[str(book)+"."+stop] = 1
     

f.close()

speechlems = {}
speechwords = 0
narrlems = {}
narrwords = 0
thuclems = {}

f = open("thucunimorphs.txt","r")
for l in f:
   if(re.search('syntactic',l) or re.search('punct',l) or re.search('^[a-zA-Z]',l)):
    continue
   #if( not re.search('NL>[VP]',l)):
    #continue
   a = l.split('\t')
   if(len(a) < 11):
    continue
   curlemma = a[4]
   curdef = a[6]
   chapsect = re.sub('([0-9]\.)[0]*([1-9][0-9]*)\..*','\g<1>\g<2>',a[5])
   if( curlemma in thuclems):
    thuclems[curlemma] = thuclems[curlemma] + 1
   else:
    thuclems[curlemma] = 1
   if( chapsect in inspeech ):
     if( curlemma in speechlems):
      speechlems[curlemma] = speechlems[curlemma] + 1
     else:
      speechlems[curlemma] = 1
     speechwords = speechwords + 1
   else:
     if (curlemma in narrlems):
      narrlems[curlemma] = narrlems[curlemma] + 1
     else:
      narrlems[curlemma] = 1

     narrwords = narrwords + 1

print(narrwords,speechwords)

speechavg = {}
narravg = {}

for foo in speechlems:
   avg =  re.sub('(\.[0-9]).*','\g<1>',str(speechlems[foo]*10000/speechwords))
   speechavg[foo] = avg
   #print(avg,speechlems[foo],foo,"speech",sep="\t")

for foo in narrlems:
   avg =  re.sub('(\.[0-9]).*','\g<1>',str(narrlems[foo]*10000/narrwords))
   narravg[foo] = avg
   #print(avg,narrlems[foo],foo,"narrative",sep="\t")

for foo in thuclems:
   if(foo not in narravg):
      navg = 0
   else:
      navg = narravg[foo]
   if(foo not in speechavg):
      savg = 0
   else:
      savg = speechavg[foo]
   if( thuclems[foo] < 11):
    continue

   if( savg):
     diff = re.sub('(\.[0-9]).*','\g<1>',str(float(navg) / float(savg)))
   else:
     diff = '1000'
   
   if( foo in lexicalentries):
     shortdef = lexicalentries[foo]
   else:
     shortdef = 'nodef'
   print(diff,navg,savg,thuclems[foo],foo,shortdef,sep="\t")
