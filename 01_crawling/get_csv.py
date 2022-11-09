import json
import csv
import os
import pandas as pd

path = 'data/mbti/json' # 데이터 위치
files = os.listdir(path)

# Json 파일을 정리하여 CSV 파일로 저장한다.
# 이유는 MBTI 컬럼이 존재하기 때문에  MBTI 별 곡 갯수를 그룹핑할 필요가 없어졌다.
for file in files:
    with open(f'{path}/{file}', 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)
        filename = file.split('.')[0]

    with open(f'data/mbti/csv/{filename}.csv', 'w', encoding='utf-8') as output_file:

        f = csv.writer(output_file)

        for i in range(0, len(data)):
            f.writerow([
                data[f"{i}"]['track_id'], 
                data[f"{i}"]['track_name'], 
                data[f"{i}"]['track_artist'], 
                data[f"{i}"]['track_image'],
                data[f"{i}"]['audio_features']['danceability'],
                data[f"{i}"]['audio_features']['energy'],
                data[f"{i}"]['audio_features']['key'],
                data[f"{i}"]['audio_features']['loudness'],
                data[f"{i}"]['audio_features']['mode'],
                data[f"{i}"]['audio_features']['speechiness'],
                data[f"{i}"]['audio_features']['acousticness'],
                data[f"{i}"]['audio_features']['instrumentalness'],
                data[f"{i}"]['audio_features']['liveness'],
                data[f"{i}"]['audio_features']['valence'],
                data[f"{i}"]['audio_features']['tempo'],
                data[f"{i}"]['mbti'],
                ])


# CSV 파일을 하나로 통합(concat)하여 tracks 라는 csv 파일을 만든다.
data = pd.DataFrame()
lists = os.listdir('./data/mbti/csv')
for i in lists:
    PATH = "./data/mbti/csv/" + i 
    add = pd.read_csv(PATH, names = ['track_id', 'title', 'artist', 'image', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'mbti']) # 파일을 하나하나 읽어옴
    data = pd.concat([data, add]) #
    data.drop_duplicates('track_id', inplace=True, keep='first') # 중복 데이터 제거
    data.to_csv('./data/mbti/tracks.csv', index=False)

