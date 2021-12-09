from pymongo import MongoClient
import json

HOST = 'tracksdb.zxoge.mongodb.net'
USER = 'dustins3'
PASSWORD = 'dkrak3105'
DATABASE_NAME = 'myFirstDatabase'
COLLECTION_NAME = 'mbti_tracks' # 컬렉션 명은 새로 지정
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

#데이터베이스와 연결한 뒤 Collection 이라는 테이블과 연결하는 작업이 가장 오래걸리실 겁니다.

with open('../scraping/json_data/data.json') as f :
    features = json.load(f)

with open('../scraping/json_data/data_info2.json') as f :
    info = json.load(f)



def track_db():
    """
    ## 트랙의 특성 (energy, mode, acousticness, id등 DB에 저장하기)
    """
    COLLECTION_NAME = 'tracks_features'
    client = MongoClient(MONGO_URI) # URI 정보를 Client 에 직접 연결
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]
    for mbti in list(features):
        collection.insert_many(documents = features[f'{mbti}']['audio_features'])


def info_db():
    """
    ## 트랙의 정보 (artistname, songname, album, type(mbti), id등 DB에 저장하기)
    """
    COLLECTION_NAME = 'tracks_info' # connet
    client = MongoClient(MONGO_URI) # URI 정보를 Client 에 직접 연결
    database = client[DATABASE_NAME] # db = client.myFirstDatabase 형식 으로도 사용 가능
    collection = database[COLLECTION_NAME] # `COLLECTION_NAME`으로 콜렉션 생성
    for mbti in list(info):
            collection.insert_many(documents = info[f'{mbti}']['tracks'])

# track_db()
# info_db()


client = MongoClient(MONGO_URI) 
db = client[DATABASE_NAME] 


