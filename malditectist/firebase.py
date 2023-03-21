import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'malditectist-3ba37.appspot.com'
})
bucket = storage.bucket()

if bucket.exists():
    print('Firebase Storage connected successfully!')
else:
    print('Error connecting to Firebase Storage.')
