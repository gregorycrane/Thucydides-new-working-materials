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
forms = {}

formquizbk2 = {}
f = open("thucunimorphs.txt","r")
for l in f:
   a = l.split('\t')
   m = re.search('(pres|imperf|aor|fut|futperf|perf|plup)\s+(ind|part|inf|opt|subj|imperat)\s+([a-z]+)\s+([1-3a-z]+\s+[a-z ]+)',l)
   if( not m or re.search('punct',l)):
     continue
   tense = m[1]
   mood = m[2]
   voice = m[3]
   if( mood == "inf"):
    numpers = ''
   else:
    numpers = m[4]
   n = re.search('>[VP] ([^\s]+),',l)
   if(n):
     useform = r.beta_code(re.sub('[+_]','',n[1]))
   else:
     useform = a[3]
   p = re.search('\s([^<\s]+)<.NL>',l)
   if(p):
    stemtype = re.sub(',.+','',p[1])
   else:
    stemtype = "nostemtype"
   if( re.search('ν$',useform) and re.search("nu_movable",l)):
     useform = re.sub('ν$','',useform)
   curlemma = a[4]
   curdef = a[6]
   curppart = curlemma  + "\t" + stemtype
   curid = curlemma + "\t" + stemtype + "\t" + tense + "\t" + voice + "\t" + mood + "\t"  + numpers + "\t" + useform + "\t" +  curdef
   lemdefs[curlemma] = curdef

   if(curid in formcount):
    formcount[curid] = formcount[curid] + 1
   else:
    formcount[curid] =  1

   if(curppart in pparts):
    pparts[curppart] = pparts[curppart] + 1
   else:
    pparts[curppart] =  1
   if(curlemma in lemcount):
    lemcount[curlemma] = lemcount[curlemma] + 1
   else:
    lemcount[curlemma] =  1

   if( re.search('\t2\.0(0[1-9]|10)',l)):
    quizkey = curdef  + ': ' + tense + " " + mood + " " + voice + " "  + numpers 
    formquizbk2[quizkey] = useform
    if(curid in formcountbk2):
     formcountbk2[curid] = formcountbk2[curid] + 1
    else:
     formcountbk2[curid] =  1
    if(curppart in ppartsbk2):
     ppartsbk2[curppart] = ppartsbk2[curppart] + 1
    else:
     ppartsbk2[curppart] =  1
    if(curlemma in lemcountbk2):
     lemcountbk2[curlemma] = lemcountbk2[curlemma] + 1
    else:
     lemcountbk2[curlemma] =  1


f = open("thuc2.1-10-verbs.txt",'w')
print("verbs in thuc. 2.1-10",file=f)
print("freq. in Thuc.","freq. in Thuc. 2","short def","lexeme",sep="\t",file=f)
for foo in sorted(lemcountbk2):
  print(lemcount[foo],lemcountbk2[foo],lemdefs[foo],foo,sep="\t",file=f)
f.close()

f = open("thuc2.1-10-vbforms1.txt",'w')
print("forms in thuc. 2.1-10",file=f)
for foo in sorted(formcountbk2):
  a = foo.split('\t') 
  curlem = a[0]
  curppart = a[0] + "\t" + a[1]
  #if( curlem in lemcountbk2 and foo in formcountbk2 and curppart in ppartsbk2 ):
  print(lemcount[curlem],formcount[foo],formcountbk2[foo],foo,sep="\t",file=f)

f.close()

f = open("thuc2.1-10-vbforms1a.txt",'w')
for foo in sorted(formquizbk2):
   print(formquizbk2[foo],foo,sep="\t",file=f)
f.close()

f = open("thuc2.1-10-vbforms2.txt",'w')
print("variations on forms and stems in thuc. 2.1-10",file=f)
for foo in sorted(formcount):
  a = foo.split('\t') 
  curlem = a[0]
  curppart = a[0] + "\t" + a[1]
  if( foo in formcountbk2):
    bk2 = formcountbk2[foo]
  else:
    bk2 = 0
  if( curlem in lemcountbk2 and curppart in ppartsbk2 ):
    print(lemcount[curlem],formcount[foo],bk2,foo,sep="\t",file=f)

f.close()


f = open("thuc2.1-10-vbforms3.txt",'w')
print("variations on forms with new stems in thuc. 2.1-10",file=f)
for foo in sorted(formcount):
  a = foo.split('\t') 
  curlem = a[0]
  curppart = a[0] + "\t" + a[1]
  if( foo in formcountbk2):
    bk2 = formcountbk2[foo]
  else:
    bk2 = 0
  if( curlem in lemcountbk2 and not curppart in ppartsbk2 ):
    print(lemcount[curlem],formcount[foo],bk2,foo,sep="\t",file=f)

f.close()

