import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# Initialize the Firebase app with the service account credentials
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'malditectist-3ba37.appspot.com'
})

# Get a reference to the default bucket
bucket = storage.bucket()

# Check if the bucket exists and connection
if bucket.exists():
    print('Firebase Storage connected successfully!')
else:
    print('Error connecting to Firebase Storage.')
