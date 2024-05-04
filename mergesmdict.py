from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

persents = {}
toposents = []
besthits = {}
bestlinks = {}
xceptions = {
'Ἀθῆναι': 'Athens',
'Ἀθηναῖος': 'Athenian',
'Αἰγινήτης': 'Aeginetan',
'Αἴγυπτος': 'Egypt',
'Αἰτωλοί': 'Aetolian',
'Αἴνιος': 'Aenian',
'Ἀκαρνάν': 'Acharnanian',
'Ἀλκαῖος': 'Alcaeus',
'Ἀκραγαντῖνος': 'Agrigentine',
'Ἀχαϊκός': 'Achaean',
'Ἀπόλλων': 'Apollo',
'Ἀργεῖος': 'Argive',
'Ἄργος': 'Argos',
'Ἀρκάς': 'Arcadian',
'Βοιωτός': 'Boeotian',
'Βυζάντιος': 'Byzantine',
'Γαῖα': 'Earth',
'Δαναός': 'Danaan',
'Δήλιος': 'Delian',
'Δῆλος': 'Delos',
'Δῖον': 'Dium',
'Δωριεύς': 'Dorian',
'Δωρικός': 'Dorian',
'Δωριακός': 'Dorian',
'Εἵλως': 'Helot',
'Ἐορδός': 'Eordian',
'Ἔρυξ': 'Eryx',
'Εὔξεινος': 'Euxine',
'Ἠδῶνες': 'Edonians',
'Θεσσαλός': 'Thessalian',
'Θηβαῖος': 'Theban',
'Θρᾷξ': 'Thracian',
'Θρᾳκία': 'Thrace',
'Ἴβηρ': 'Iberian',
'Ἴλιος': 'Ilium',
'Ἰλλυρικός': 'Illyrian',
'Ἱππωνιεύς': 'Hipponian',
'Ἴστρος': 'Danube',
'Ἰταλία': 'Italy',
'Ἰταλιώτης': 'Italian',
'Ἴωνες': 'Ionian',
'Κάρ': 'Carian',
'Καρχηδών': 'Carthage',
'Κέρκυρα': 'Corcyra',
'Κερυκυραῖος': 'Corcyrian',
'Κορίνθιος': 'Corinthian',
'Κόρινθος': 'Corinth',
'Κρής': 'Cretan',
'Κρητικός': 'Cretan',
'Κροῖσος': 'Croesus',
'Κύζικος': 'Cyzicene',
'Κύμη': 'Cyme',
'Λακεδαιμόνιος': 'Lacedaemonian',
'Λέσβιος': 'Lesbian',
'Λιβύη': 'Libya',
'Λύκαιον': 'Lycaeum',
'Λαύρειον': 'Laurium',
'Μακεδών': 'Macedonian',
'Μασσαλία': 'Marseilles',
'Μεγαρεύς': 'Megarian',
'Μουνιχίη': 'Munychia',
'Μηδικός': 'Median',
'Μῆδος': 'Mede',
'Μῆλος': 'Melos',
'Μυκήνη': 'Mycenae',
'Νισαῖος': 'Nisaea',
'Ὀπόεις': 'Opous',
'πνύξ': 'Pnyx',
'Ξέρξης': 'Xerxes',
'Παίων': 'Paeonian',
'Πελαργικός': 'Pelasgian',
'Πελοποννήσιος': 'Peloponnesian',
'Πελοπόννησος': 'Peloponnese',
'Πέρσης': 'Persian',
'Πλαταιεύς': 'Plataean',
'Πλαταιικός': 'Plataean',
'Πύλος': 'Pylos',
'Ῥηγῖνος': 'Rhegian',
'Ῥήγιον': 'Rhegium',
'Ῥίον': 'Rhium',
'Σάμος': 'Samos',
'Σάμιος': 'Samian',
'Σεγεσταῖος': 'Egestean',
'Σικανός': 'Sicanian',
'Σικελία': 'Sicily',
'Σικελικός': 'Sicilian',
'Σικελιώτης': 'Sicilian',
'Σικυώνιος': 'Sicyonian',
'Συρακοῦσαι': 'Syracuse',
'Τάρας': 'Tarentum',
'Τροία': 'Troy',
'Τρωικός': 'Trojan',
'Τρώς': 'Trojan',
'Ὅμηρος': 'Homer',
'Φοῖνιξ': 'Phoenician',
'Φοινίκη': 'Phoenicia',
'Φοινικικός': 'Phoenician',
'Φωκαιεύς': 'Phocaieus',
'Χάων': 'Chaonian',
'Χῖος': 'Chios',
'Χαλκιδεύς': 'Chalcidian'
}

r = Replacer()

allthucents = {} 

f = open("thucents.txt","r")
for l in f:
  l = re.sub('\s+$','',l)
  allthucents[l] = 1
  args = l.split('\t')
  if (args[2] == 'Ἕλλην' or args[2] == 'Ἑλλάς' or args[2] == 'Εὐρώπη'):
    continue
  if( breathing(args[2]) == Breathing.ROUGH and not re.search('[ῥῬ]',args[2])):
   xlit = 'H' + unidecode(args[2]).lower()
  else:
   xlit = unidecode(args[2])
  xlit = re.sub('kh','ch',xlit)
  xlit = re.sub('k','c',xlit)
  xlit = re.sub('Kh','Ch',xlit)
  xlit = re.sub('K','C',xlit)
  xlit = re.sub('Cs','X',xlit)
  xlit = re.sub('([bcdfghklmnprstwBCDFGHKLMNPRSTW])u([bcdfghklmnprstwBCDFGHKLMNPRSTW])','\g<1>y\g<2>',xlit)
  if( not re.search('person',l)):
   xlit = re.sub('aios$','aean',xlit)
   xlit = re.sub('aion$','aeum',xlit)
   xlit = re.sub('aioi$','aeans',xlit)
   xlit = re.sub('eios$','eian',xlit)
   xlit = re.sub('eioi$','eians',xlit)
   xlit = re.sub('ios$','ian',xlit)
   xlit = re.sub('os$','us',xlit)
   xlit = re.sub('gg','ng',xlit)

  if( args[2] in xceptions):
    xlit = xceptions[args[2]]
  if( args[2] == 'Ἀττικός' and re.search('fem:',l)):
    xlit = 'Attica'
  if( args[2] == 'Ἀργεῖος' and re.search('fem:',l)):
    xlit = 'Argolis'
  if( args[2] == 'Λακωνικός' and re.search('fem:',l)):
    xlit = 'Laconia'
  if( re.search('eus$',xlit) and re.search('ethnic',args[1])):
    xlit = re.sub('eus$','ean',xlit)
  persents[l] = xlit

f.close()
f = open("smithdictent.txt","r")
curcit = ''
for l in f:
  if( not re.search('Thuc\.',l)):
   continue
  l = re.sub('\s+$','',l)
  toposents.append(l) 

f.close()

limit = 1000
sawents = 0
for foo in persents:
   #if( not re.search('^2\.',foo)):
    #continue
   sawents = 1 + sawents
   args = foo.split('\t')
   lem1 = args[2]
   curcit2 = re.sub('([0-9]+\\.[0-9]+).*','Thuc. ' + '\g<1> ',args[0])
   #print('cits',args[0],args[2],curcit2,'zz',sep='-')
   for boo in toposents:
     if( re.search(curcit2,boo)):
       a2 = boo.split()
   #    print("cit2",curcit2,a2[4],boo)
       xlit = persents[foo]
       lem2 = a2[4]
       #r = fuzz.ratio(a2[3],xlit)
       r = fuzz.ratio(a2[4],args[2])
       if( foo in besthits ):
         if(r > besthits[foo] ):
           besthits[foo] = r
           bestlinks[foo] = boo
           #print("hit2",r,lem1,lem2)
       else:
         besthits[foo] = r
         bestlinks[foo] = boo
         #print("hit1",r,xlit,a2[4],curcit,boo)

totbest = 0
for tmp in bestlinks:
   totbest =  besthits[tmp] + totbest

if( sawents > 0):
 avg = totbest/sawents
else:
 avg = 0
print('avg fit',sawents,avg)

for tmp in bestlinks:
   c1 = re.sub(r'^(..).*','\g<1>',persents[tmp]) 
   args1 = tmp.split()
   args = bestlinks[tmp].split()
 
   if( besthits[tmp] < 50 or (besthits[tmp] < 71 and not  re.search('^' + c1 ,args[3]))):
       #print( besthits[tmp],'reject',persents[tmp],args[3],tmp,bestlinks[tmp])
       print( besthits[tmp],'reject',args1[2],args[4],tmp,bestlinks[tmp])
   else:
       allthucents[tmp] = 2
       print(besthits[tmp],'keep',args1[2],args[4],tmp,bestlinks[tmp])
   #print(besthits[tmp],persents[tmp],tmp,bestlinks[tmp],del='\t')

for foo in allthucents:
   if( allthucents[foo] == 1 ):
    print("nosmith",foo)

