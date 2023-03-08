import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'malditectist-3ba37.appspot.com'
})
bucket = storage.bucket()

# def upload_file_to_firebase(file_path, destination_blob_name):
#     bucket = storage.bucket()
#     blob = bucket.blob(destination_blob_name)
#     blob.upload_from_filename(file_path)
#     return blob.public_url

if bucket.exists():
    print('Firebase Storage connected successfully!')
else:
    print('Error connecting to Firebase Storage.')
