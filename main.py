import requests
import uuid
import firebase_admin
from firebase_admin import credentials, firestore, storage
from scraper import Scraper 

def save_fb_storage(uri: str, bucket: storage):
    image_data = requests.get(uri).content
    img_file_name = str(uuid.uuid4())
    blob = bucket.blob(f"{img_file_name}.jpg")
    blob.upload_from_string(
            image_data,
            content_type='image/jpg'
        )
    blob.make_public()
    return blob.public_url

## About Firestore

def create_firestore(doc: dict, db: firestore):
    db.collection(u'raffles').add(doc)
    
def read_firestore(db: firestore):
    docs = db.collection(u'raffles').stream()  
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
        
def delete_firestore(db: firestore):
    docs = db.collection(u'raffles').stream()  
    for doc in docs:
        doc.reference.delete()

## About Bucekt 
def delete_bucket(bucket: storage):
    blobs = bucket.list_blobs()
    for b in blobs:
        b.delete()


if __name__ == "__main__":
    scraper = Scraper()
    # 스크랩
    receivers = []
    arr = []
    arr += scraper.get_lucky()
    arr += scraper.get_shoe_prize()

    ## 파이어베이스 시작 영역
    cred = credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(cred, {
        "storageBucket": "subscribe-sneaker.appspot.com"
    })

    db = firestore.client()
    bucket = storage.bucket()

    ## db 초기화
    delete_firestore(db)
    delete_bucket(bucket)

    ## UPLOAD 영역 
    for raffle in arr:
        new_data = {
            'img': save_fb_storage(raffle["img"], bucket),
            'content': raffle["content"],
            'link': raffle["link"]
        }
        create_firestore(new_data, db)