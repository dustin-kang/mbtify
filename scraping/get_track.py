# -*- coding: utf-8 -*-

import json
import requests
import base64
from secrets import *
from get_api import getAccessToken, gettrackAudioFeatures



with open('./json_data/mbti_track/mbti_tracks.json') as f :
    mbti_tracks = json.load(f)


tracks_features = {}
token = getAccessToken(clientID, clientSecret)

for mbti in list(mbti_tracks):
    with open(f'./json_data/mbti_track/{mbti}.json') as f :
        tracks = json.load(f)
    ids = str(list(tracks.values())).replace('\'','').replace('[','').replace(' ','').replace(']','').replace(',','%2C')
    tracks_features[f'{mbti}'] = gettrackAudioFeatures(token, ids)



with open(f'./json_data/dataff.json','w') as f:
   json.dump(tracks_features, f)


"""
gettrackAudioFeatures가 정상적으로 실행이 되지 않음.
->> SPotify API CONSOL을 이용하여 TrackIDs 값과 Token으로 아래 두가지 파일들을 만들어 냈습니다.
- data.json : 음악의 세부 특징을 담은 파일
- data_info.json : 음악의 가수, 앨범등의 정보를 담은 파일

"""
