from google.cloud import firestore

db = firestore.Client()

doc_ref = db.collection(u'users').document(u'alovelace')

doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1915
})

# users_ref = db.collection(u'users')
# docs = users_ref.get()

# for doc in docs:
# print(u'{} => {}'.format(doc.id, doc.to_dict()))
