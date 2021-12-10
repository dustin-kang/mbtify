import csv, sqlite3
import pandas as pd
import warnings

"""
## MongoDb Compass -> Sqlite3

- MongoDB Compass를 이용하여 DB 파일을 csv 파일로 변경하고 csv 파일을 rdb로 저장 
- 데이터를 정형화 함.
- Schema 형식으로 설계함.
"""

warnings.filterwarnings(action='ignore') 

# field 명을 변경하고 문자열 수정을 위한 pandas 작업
info = pd.read_csv('./tracks_info.csv')

for i in range(0, len(info)):
  info['album.artists'][i] = info['album.artists'][i].split("\"name\":\"")[1].split("\",\"type\"")[0]
  info['album.images'][i] = info['album.images'][i].split("640,\"url\":\"")[1].split("\",\"width\"")[0]

info.rename(columns={"album.artists" : "artist", "album.images" : "image_url", "album.release_date" : "release_date", "type" : "mbti"}, inplace=True)
info.to_csv('./tracks_info2.csv', index=False)


# csv 파일을 sqlite db에 옮기는 작업
connect = sqlite3.connect("tracks.db")
cur = connect.cursor()
cur.execute(""" CREATE TABLE features_table(
        _id VARCHAR(32) NOT NULL,
        id VARCHAR(32) NOT NULL, 
        danceability FLOAT,
        acousticness FLOAT,
        energy FLOAT,
        instrumentalness FLOAT,
        key INT,
        liveness FLOAT,
        loudness FLOAT,
        mode INT,
        speechiness FLOAT,
        tempo FLOAT,
        valence FLOAT,
        PRIMARY KEY (_id)
        );
    """)

cur.execute(""" CREATE TABLE info_table(
        _id VARCHAR(32) NOT NULL,
        id VARCHAR(32) NOT NULL, 
        artist VARCHAR(64),
        image_url VARCHAR(64),
        release_date VARCHAR(32),
        name VARCHAR(32),
        popularity INT,
        mbti VARCHAR(32),
        PRIMARY KEY (_id),
        FOREIGN KEY(id) REFERENCES features_table(id)
        );
    """)

with open('./tracks_features.csv', 'rt') as f:
    features =  csv.DictReader(f)
    to_ft = [(i['_id'], i['id'], i['danceability'], i['acousticness'], i['energy'], i['instrumentalness'], i['key'], i['liveness'], i['loudness'],
        i['mode'], i['speechiness'], i['tempo'], i['valence']) for i in features]

with open('./tracks_info2.csv', 'rt') as f:
    info =  csv.DictReader(f)
    to_if = [(i['_id'], i['id'], i['artist'], i['image_url'], i['release_date'], i['name'], i['popularity'], i['mbti']) for i in info]

cur.executemany("INSERT INTO features_table (_id, id, danceability, acousticness, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, valence) VALUES (?, ?,  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_ft)
cur.executemany("INSERT INTO info_table (_id, id, artist, image_url, release_date, name, popularity, mbti) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_if)
connect.commit()
connect.close
