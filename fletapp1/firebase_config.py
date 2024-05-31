# firebase_config.py
# import pyrebase

import firebase_admin
from firebase_admin import credentials, firestore, auth, storage

cred = credentials.Certificate("C:/Users/javie/Documents/UNI/TFG/app-control-de-acceso-service-account.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'app-control-de-acceso-1ab28.appspot.com'
})

# Inicializar Firestore Database y Storage
db = firestore.client()
bucket = storage.bucket()

