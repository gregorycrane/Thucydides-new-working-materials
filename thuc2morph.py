import re


curchap = 0
curbook = 0
cursect = 0
thucall = {}
thuc2 = {}
thuc2tot = 0
thuctot = 0
thucwords = []

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
    if( curlemma in thuc2 ):
     thuc2[curlemma] = thuc2[curlemma] + 1
    else:
     thuc2[curlemma] = 1

#  print(curform,curlemma,curparad,l)
  
vtots = {}
thucallvs2 = thuctot/thuc2tot
print("thuc whole vs thuc 2", thuc2tot,thuctot,thucallvs2)
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
'πως2': 'πως',
'στυράκιον': 'στύραξ2',
'συνεπιλαμβάνομαι': 'συνεπιλαμβάνω',
'σώζω': 'σῴζω',
}
curdef = ''
for foo in thucwords:
  if( re.search('syntacticb',foo)):
   print(foo,end='')
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
  restline = re.sub('.+(<NL>.+)','\g<1>',foo)
  if( a[1] in vtots):
   print(vtots[a[1]],a[0],a[1],a[2],curdef,restline,sep='\t',end='')
  else:
   print('0\t0\t0\tpunct',a[0],a[1],a[2],'punct',restline,sep='\t',end='')
   #print('0\t0\t0\tpunct', foo,sep='\t',end='')
   
