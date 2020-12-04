from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from cltk.tokenize.greek.sentence import SentenceTokenizer
from fuzzywuzzy import fuzz
import re

r = Replacer()
sent_tokenizer = SentenceTokenizer()


f = open("1thucunimorphs.txt")
import stanza


if( 1 ):
 processor_dict = {
    'tokenize': 'perseus',
    'mwt': 'perseus',
    'pos': 'perseus',
    'lemma': 'perseus',
    'depparse': 'perseus'
 }
 outf = open("thuc.tb.perseus.txt","w")
 print('# https://stanfordnlp.github.io/stanza/neural_pipeline.html with perseus model for ancient Greek',file=outf)
 idbase = '0003.001-'
else:
 processor_dict = {
    'tokenize': 'proiel',
    'mwt': 'proiel',
    'pos': 'proiel',
    'lemma': 'proiel',
    'depparse': 'proiel'
 }
 outf = open("thuc.tb.proiel.txt","w")
 print('# https://stanfordnlp.github.io/stanza/neural_pipeline.html with proiel model for ancient Greek',file=outf)
 idbase = '0003.001-'

stanza.download('grc', processors=processor_dict, package='perseus')
nlp_grc = stanza.Pipeline('grc', processors=processor_dict, package='perseus')


#gr = nlp_grc(' τί ἦν κλαγγὴ δεινὴ ἐv Χρύσῃ καλῇ ;') 
#gr = nlp_grc(' ἢν δέ που μορίῳ τινὶ προσμείξωσι, κρατήσαντές τέ τινας ἡμῶν πάντας αὐχοῦσιν ἀπεῶσθαι καὶ νικηθέντες ὑφ᾽ ἁπάντων ἡσσῆσθαι.') 

#gr = nlp_grc(' Ἡροδότου Ἁλικαρνησσέος ἱστορίης ἀπόδεξις ἥδε, ὡς μήτε τὰ γενόμενα ἐξ ἀνθρώπων τῷ χρόνῳ ἐξίτηλα γένηται, μήτε ἔργα μεγάλα τε καὶ θωμαστά, τὰ μὲν Ἕλλησι τὰ δὲ βαρβάροισι ἀποδεχθέντα') 
#print(gr)
#gr = nlp_grc('οὔκουν χρή, εἴ τῳ καὶ δοκοῦμεν πλήθει ἐπιέναι καὶ ἀσφάλεια πολλὴ εἶναι μὴ ἂν ἐλθεῖν τοὺς ἐναντίους ἡμῖν διὰ μάχης, τούτων ἕνεκα ἀμελέστερόν τι παρεσκευασμένους χωρεῖν, ἀλλὰ καὶ πόλεως ἑκάστης ἡγεμόνα καὶ στρατιώτην τὸ καθ᾽ αὑτὸν αἰεὶ προσδέχεσθαι ἐς κίνδυνόν τινα ἥξειν.') 

curcit = ''
lastcit = ''
uniqforms2 = {}
formlemmas = {}

def printgr(gr):
       wlist = gr.to_dict()
       altlemma = ''
       for foo in wlist[0]:
         curf = foo['text']
         tmpuniq = lastcit + '@' + foo['text']
         if( tmpuniq in uniqforms2):
           uniqforms2[tmpuniq] = uniqforms2[tmpuniq] + 1
         else:
           uniqforms2[tmpuniq] =  1
         curuniq = tmpuniq + '[' + str(uniqforms2[tmpuniq]) + ']'

         for foo2 in foo:
          if( foo2 == 'deprel'):
            print(foo[foo2]+'\t-\t',end="\t",file=outf)
          else:
           if( foo2 == 'misc'):
            altlemma = ''
            if( not foo['upos'] == 'PUNCT'):
             if( curuniq in formlemmas):
              if( not formlemmas[curuniq] == foo['lemma']):
               altlemma = '|altlem='+formlemmas[curuniq]
            print(foo[foo2]+'|'+curuniq+altlemma,end="\n",file=outf)
           else:
            print(foo[foo2],end="\t",file=outf)

uniqids = {}
uniqforms = {}
#print(gr)
curline = ''
sentid = 1
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
       print("\n# sent_id = ",lastcit+':'+str(sentid),file=outf)
       sentid = sentid + 1
       print("# cite =Thuc.",lastcit,file=outf)
       print("$ text =",s,file=outf)
       gr = nlp_grc(s)
       printgr(gr)
      curline = ''
     lastcit = curcit
  curline = curline + ' ' + a[0]
  tmpuniq = lastcit + '@' + a[0]
  if( tmpuniq in uniqforms):
       uniqforms[tmpuniq] = uniqforms[tmpuniq] + 1
  else:
       uniqforms[tmpuniq] =  1
  curuniq = tmpuniq + '[' + str(uniqforms[tmpuniq]) + ']'
  formlemmas[curuniq] = a[1]
  #print('current',curline)

print(lastcit,curline,file=outf)
gr = nlp_grc(curline)
printgr(gr)
