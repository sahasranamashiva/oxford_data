import sys
from google.cloud import firestore

db = firestore.Client()

doc_ref = db.collection(u'word').document(sys.argv[1])

word = doc_ref.get()

print(u'{} => {}'.format(word.id, word.to_dict()))
# print('Part of Speech: '+word.POS)
# print('Phonetic: '+word.Phonetic)
