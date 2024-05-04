import re
from cltk.tokenize.greek.sentence import SentenceTokenizer
sent_tokenizer = SentenceTokenizer()


curchap = 0
curbook = 0
cursect = 0
thucall = {}
thuc2 = {}
thuc2cits = {}
thuc2tot = 0
thuctot = 0
thucwords = []
thucdefs = {}

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

sentid = 1
f = open("1thucunimorphs.txt","r")
curparad = ''
for l in f:
  thucwords.append(l)
  if( re.search('syntacticb',l)):
   continue
  m = re.search('([^\s<]+)<\/NL>',l)
  if( m):
    curparad = m.group(1)
  args = l.split('\t')
  if( re.search('punct',l)):
   curform = args[0]
   curlemma = args[1]
  else:
   thuctot = thuctot + 1
   curlemma = args[1]
   curform = args[0]
   if( curlemma in thucall ):
    thucall[curlemma] = thucall[curlemma] + 1
   else:
    thucall[curlemma] = 1
   if( re.search('^2\.00[1-9]', args[2]) or re.search('^2\.01[0-1]', args[2]) or re.search('^2\.03[4-9]', args[2])):
    thuc2tot = thuc2tot + 1
    workcit =  re.sub('([0-9]\.)[0]*([0-9]+)\-.+','\g<1>\g<2>',args[2])
    workcit = re.sub('\.[0]+','.',workcit)
    if( curlemma in thuc2 ):
     thuc2[curlemma] = thuc2[curlemma] + 1
     if( thuc2[curlemma] < 10):
        thuc2cits[curlemma] = thuc2cits[curlemma] + '; ' + workcit
    else:
     thuc2[curlemma] = 1
     thuc2cits[curlemma] =  workcit

#  print(curform,curlemma,curparad,l)
  
vtots = {}
thucallvs2 = thuctot/thuc2tot
#print("thuc whole vs thuc 2", thuc2tot,thuctot,thucallvs2)
for foo in thuc2:
  expected = re.sub('(\.[0-9][0-9]).*','',str(thucallvs2 * thuc2[foo]))
  vtots[foo] = str(thuc2[foo]) + "\t" +  str(thucall[foo]) + "\t" + str(expected)
  #print(foo,vtots[foo])

f.close()
xceptions = {

'Βοιωταρχέω': 'βοιωταρχέω',
'διαβουλεύομαι': 'διαβουλεύω',
'ἔσοδος': 'εἴσοδος',
'θνήσκω': 'θνῄσκω',
'ποτέ': 'ποτε',
'πως2': 'πως',
'στυράκιον': 'στύραξ2',
'συνεπιλαμβάνομαι': 'συνεπιλαμβάνω',
'σώζω': 'σῴζω',
}
curdef = ''
for foo in thucwords:
  if( re.search('syntacticb',foo)):
   #print(foo,end='')
   continue
  a = foo.split('\t')
  lemlook = a[1]
  if( re.search('1',a[1])):
    lemlook = re.sub('1','',a[1])
  if( re.search('λέγω[123]',a[1])):
    lemlook = 'λέγω'
  if( lemlook in xceptions):
    lemlook = xceptions[lemlook]
  if( lemlook in lexicalentries ):
   curdef = lexicalentries[lemlook]
  else:
    curdef = 'nodef'
  thucdefs[a[1]] = curdef
  restline = re.sub('.+(<NL>.+)','\g<1>',foo)
  #if( a[1] in vtots):
  # print(vtots[a[1]],a[0],a[1],a[2],curdef,restline,sep='\t',end='')
  #else:
  # print('0\t0\t0\tpunct',a[0],a[1],a[2],'punct',restline,sep='\t',end='')
   #print('0\t0\t0\tpunct', foo,sep='\t',end='')
   
#for foo in sorted(thuc2):
  #print('vocab',foo,thucdefs[foo],thuc2[foo], thuc2cits[foo],sep="\t")
curline = ''
curcit = ''
lastcit = ''
uniqforms = {}
formlemmas = {}
sentwords = 0
knownwords = 0
f = open("1thucunimorphs.txt")
for l in f:

  if(re.search('^start',l)):
    continue
  a = l.split('\t')
  if( re.search('syntacticbreak',l )):
    if( a[0] == ':'):
     a[0] = '·'
    curline = curline + ' ' + a[0]
    continue
  if( len(a) < 4):
    continue
  m = re.search('^([0-9]\.)[0]*([1-9][0-9]*\.[0-9]+)',a[2])
  if( m ):
    curcit = m[1] + m[2]
    if( not curcit == lastcit ):
     if(curline and lastcit):
      curline = re.sub('^[ ]+','',curline)
      curline = re.sub('[ ]+([,\.:·])','\g<1>',curline)
      sents = sent_tokenizer.tokenize(curline)
      for s in sents:
       print("# sent_id = ",lastcit+':'+str(sentid))
       sentid = sentid + 1
       print("# cite =Thuc.",lastcit)
       print("# " + str(sentwords) + ' ' + str(knownwords) + " text =",s,"\n")
       sentwords = 0
       knownwords = 0
      curline = ''
     lastcit = curcit
  if( a[1] in thuc2):
   curline =  curline +  ' '  + a[0] 
   knownwords = knownwords + 1
   sentwords = sentwords + 1
   print(a[1],thucall[a[1]],thuc2cits[a[1]])
  else:
   if( not re.search('[a-z]',a[1])):
    print(a[1],thucall[a[1]],thucdefs[a[1]])
    sentwords = sentwords + 1
   curline = curline + ' ' + a[0]
  tmpuniq = lastcit + '@' + a[0]
  if( tmpuniq in uniqforms):
       uniqforms[tmpuniq] = uniqforms[tmpuniq] + 1
  else:
       uniqforms[tmpuniq] =  1
  curuniq = tmpuniq + '[' + str(uniqforms[tmpuniq]) + ']'
  formlemmas[curuniq] = a[1]
  #print('current',curline)

