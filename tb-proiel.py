from unidecode import unidecode
from greek_accentuation.characters import *
from cltk.corpus.greek.beta_to_unicode import Replacer
from fuzzywuzzy import fuzz
import re

r = Replacer()

f = open("1thucunimorphs.txt")
import stanza

processor_dict = {
    'tokenize': 'proiel',
    'mwt': 'proiel',
    'pos': 'proiel',
    'lemma': 'proiel',
    'depparse': 'proiel'
}

stanza.download('grc', processors=processor_dict, package='perseus')
nlp_grc = stanza.Pipeline('grc', processors=processor_dict, package='perseus')

il = nlp_grc('μήνιν')

il

#gr = nlp_grc(' τί ἦν κλαγγὴ δεινὴ ἐv Χρύσῃ καλῇ ;') 
#gr = nlp_grc(' ἢν δέ που μορίῳ τινὶ προσμείξωσι, κρατήσαντές τέ τινας ἡμῶν πάντας αὐχοῦσιν ἀπεῶσθαι καὶ νικηθέντες ὑφ᾽ ἁπάντων ἡσσῆσθαι.') 

#gr = nlp_grc(' Ἡροδότου Ἁλικαρνησσέος ἱστορίης ἀπόδεξις ἥδε, ὡς μήτε τὰ γενόμενα ἐξ ἀνθρώπων τῷ χρόνῳ ἐξίτηλα γένηται, μήτε ἔργα μεγάλα τε καὶ θωμαστά, τὰ μὲν Ἕλλησι τὰ δὲ βαρβάροισι ἀποδεχθέντα') 
#print(gr)
#gr = nlp_grc('οὔκουν χρή, εἴ τῳ καὶ δοκοῦμεν πλήθει ἐπιέναι καὶ ἀσφάλεια πολλὴ εἶναι μὴ ἂν ἐλθεῖν τοὺς ἐναντίους ἡμῖν διὰ μάχης, τούτων ἕνεκα ἀμελέστερόν τι παρεσκευασμένους χωρεῖν, ἀλλὰ καὶ πόλεως ἑκάστης ἡγεμόνα καὶ στρατιώτην τὸ καθ᾽ αὑτὸν αἰεὶ προσδέχεσθαι ἐς κίνδυνόν τινα ἥξειν.') 


#print(gr)
curline = ''
curcit = ''
for l in f:
  if(re.search('syntacticbreak',l)):
   if( curline):
    print(curcit,curline)
    gr = nlp_grc(curline)
    print(gr)
    curline = ''
   continue

  a = l.split('\t')
  m = re.search('^([0-9]\.)[0]*([1-9][0-9]*\.[0-9]+)',a[2])
  if( m ):
    curcit = m[1] + m[2]
  curline = curline + ' ' + a[0]
  #print('current',curline)
