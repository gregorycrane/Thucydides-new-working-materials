from cltk.corpus.greek.beta_to_unicode import Replacer
import re

r = Replacer()

curchap = 0
curbook = 0
cursect = 0
thucall = {}
thuc2 = {}
thuc2tot = 0
thuctot = 0

f = open("thucmorphs.txt","r")
curparad = ''
for l in f:
  if( re.search('syntacticb',l) or re.search('punct',l)):
   print(l,end='')
   continue
  args = l.split('\t')
  curform = r.beta_code(args[0])
  curlemma = re.sub(' ','',r.beta_code(re.sub('([0-9]+)',' \g<1>',args[1])))
  b = re.sub(r'^[^\t]+\t[^\t]+\t','',l)
  print(curform,curlemma,b,sep='\t',end='')
