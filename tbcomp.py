import re

forms = {}
lemmas = {}
poss = {}
atts = {}
deps = {}
depsb = {}
deprels = {}
fullids = {}

forms2 = {}
lemmas2 = {}
poss2 = {}
atts2 = {}
deps2 = {}
depsb2 = {}
deprels2 = {}

persforms = []
f = open("thuc.tb.proiel.txt")
for l in f:
  m = re.search('sent_id =[ ]+([0-9\.:]+)',l)
  if( m ):
   globid = 'pro-' + m[1]
#   print(globid)
  if( not re.search('^[1-9]',l) and not re.search('[0-9]@',l)):
   continue
  m = re.search('\|([1-8]\.[0-9]+\.[0-9]+@[^\|\n ]+)',l)
  if( not m):
   continue
  curid = m[1]
  curid = re.sub('[\.,:;]\[','[',curid)
  args = l.split('\t')
  fullids[globid + '.' + args[0]] = curid

  forms2[curid] = re.sub('[\.,;:]','',args[1])
  lemmas2[curid] = args[2]
  poss2[curid] = args[3]
  if( re.search('^[0-9]+$',args[5])):
   atts2[curid] = 'noatts'
   deps2[curid] = args[5]
   deprels2[curid] = args[6]
   depsb2[curid] = globid + '.' + args[5]
  else:
   atts2[curid] = args[5]
   deps2[curid] = args[6]
   deprels2[curid] = args[7]
   depsb2[curid] = globid + '.' + args[6]
  #print(curid,args[1],l,end='')
f.close()

f = open("thuc.tb.perseus.txt")
for l in f:
  m = re.search('sent_id =[ ]+([0-9\.:]+)',l)
  if( m ):
   globid = 'per-' + m[1]
  if( not re.search('^[1-9]',l) and not re.search('[0-9]@',l)):
   continue
  if( re.search('PUNCT',l)):
   continue
  m = re.search('\|([1-8]\.[0-9]+\.[0-9]+@[^\|\n ]+)',l)
  if( not m):
   continue
  curid = m[1]
  persforms.append(curid)
  args = l.split('\t')
  fullids[globid + '.' + args[0]] = curid
  lemmas[curid] = args[2]
  poss[curid] = args[4]
  if( re.search('^[0-9]+$',args[5])):
   atts[curid] = 'noatts'
   deps[curid] = args[5]
   deprels[curid] = args[6]
   depsb[curid] = globid + '.' + args[5]
  else:
   atts[curid] = args[5]
   deps[curid] = args[6]
   depsb[curid] = globid + '.' + args[6]
   deprels[curid] = args[7]
   #print(curid,args[1],l,end='')

for curid in persforms:
  badanal = ''
  if( not curid in lemmas2):
   badanal = 'nolem'
  if( curid in lemmas2 and not lemmas2[curid] == lemmas[curid]):
   badanal = lemmas2[curid]
#  if( badanal):
#    print("lemdiff",curid,lemmas[curid],badanal)
  
  badanal = ''
  if( not curid in poss2):
   badanal = 'nolem'
  if( curid in poss2 and not poss2[curid] == poss[curid]):
   badanal = poss2[curid]
#  if( badanal):
#    print("posdiff",curid,poss[curid],badanal)
  
  
  badanal = ''
  if( not curid in deps2):
   badanal = 'nolem'
  if( not re.search('^[pnavrl]',poss[curid])):
    continue
  if( not curid in deps2):
    continue
  #if( not deps2[curid] == deps[curid]):
  if( 1):
    if( re.search('\.0$',depsb2[curid])):
      badanal = 'root'
      bananal2 = ''
    else:
      badanal = fullids[depsb2[curid]]
      badanal2 = depsb2[curid]
  if( badanal):
    if( re.search('\.0$',depsb[curid])):
      persfull = 'root'
    else:
      persfull = fullids[depsb[curid]]
  if( not persfull == badanal):
     print("depdiff",curid,persfull,deprels[curid],badanal,deprels2[curid])
  else:
     print("depsame",curid,persfull,deprels[curid],badanal,deprels2[curid])
  
f.close()
