import sqlite3
import pandas as pd
import pickle

"""
DB에서 데이터셋 pandas 데이터프레임 형식으로 불러오기
"""
connect = sqlite3.connect('../db/track.db')
cursor = connect.cursor()
cursor.execute("""
SELECT ft.id, it.artist, it.name, it.image_url, it.release_date,ft.danceability,ft.acousticness,ft.energy,
		ft.key, ft.liveness, ft.loudness+60"loudness", ft.mode, ft.speechiness, ft.tempo, ft.valence, it.popularity, it.mbti 
FROM features_table ft
JOIN info_table it ON ft.id = it.id
""")

rows = cursor.fetchall()

cols = [column[0] for column in cursor.description] #컬럼마다 반복을 진행 -> column name 만 cols에 저장
df = pd.DataFrame.from_records(data=rows, columns=cols)  #data와 cols(컬럼 명)으로 데이터 프레임을 만듬.
connect.close()


"""
머신러닝 학습하기

"""
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBClassifier

def modelling(df):
    target = "mbti" # mbti를 타겟값으로 설정
    
    df_info = df[df.columns[0:5]] # data에 대해 모델링용도로 쓰이지 않을 정보
    y = df[target] # label
    X = df[df.columns[5:-1]] # data

    # 모델링
    model = make_pipeline(
        MinMaxScaler(),
        XGBClassifier()
    )

    return model

model = modelling(df)

with open('./model.pkl', 'wb') as pickle_file: # pikle을 이용하여 객체 피클링
    pickle.dump(model, pickle_file)

