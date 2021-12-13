# -*- coding: utf-8 -*-

"""
Model 적용을 위한 code
link -> data
"""
# data = "https://open.spotify.com/track/2bgTY4UwhfBYhGT4HUYStN?si=c4c4b7d47406465c"

import json
import requests
import base64
import pandas as pd
from secrets import *

from requests.api import head # secret.py에서 클라이언트 정보 가져오기

authUrl = "https://accounts.spotify.com/api/token"
authHeader = {}
authData = {}

clientID = "985bddba809c4d149f1347b928dcc4a4"
clientSecret = "fcc9d00890384342a73f252cf330f444"

def getAccessToken(clientID, clientSecret):
    """
    ## 토큰을 가져오는 함수
    """
    message = f"{clientID}:{clientSecret}" # secret.py에 사용자 정보 불러오기
    message_bytes= message.encode('ascii') # 메세지 ascii code로 인코딩
    base64_bytes = base64.b64encode(message_bytes)  
    base64_message = base64_bytes.decode('ascii')

    # print(base64_message) 
    # curl -X "POST" -H "Autorization: Basic Zj....Y0NDQ=" -d grant_type=client_credentials https://accounts.spotify.com/api/token
    # 반드시 Basic 뒤에 한칸 뛰어야 합니다.

    authHeader['Authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"

    res = requests.post(authUrl, headers=authHeader, data=authData)

    print(res) # <Response [200]> 

    responseObject = res.json() # json 파일화 시키기
    # print(json.dumps(responseObject, indent=2))  # indent 옵션 : JSON 문자열을 읽기 편하게 할 필요가 있을 경우

    # 토큰을 받았으면, 아래와 같이 토큰을 가져올 수 있습니다.

    accessToken = responseObject['access_token']

    return accessToken

token = getAccessToken(clientID, clientSecret)



# Playlist의 Tracks를 가져오는 함수를 지정하였습니다.
def getTrackFeatures(token, data):
    """
    ## 트랙의 특징과 설명을 가져오는 함수
    ### input
    `token`, `data`
    - data는 트랙의 링크를 그대로 가져오는 문자열

    ### output
    `dict_info`, `dict_data`
    - `dict_info` : 트랙에 대한 설명 (artist = string, image_url = string, song = string)
    - `dict_data` : {'danceability': 0.759, 'acousticness': 0.00323, 'energy': 0.459, 'key': 8, 'liveness': 0.0906, 'loudness': 54.813, 'mode': 1, 'speechiness': 0.0948, 'tempo': 109.997, 'valence': 0.695, 'popularity': 91}
    - `dict_data`는 판다스 형식으로 되어있다.
    """
    import pandas as pd
    import numpy as np

    # 음악 쿼리를 링크로 변환하는 API (Search)
    data = data.replace(' ', '%20')
    endpoint = f"	https://api.spotify.com/v1/search?q={data}&type=track&market=KR&limit=1"

    getHeader = {
        "Authorization" : "Bearer " + token
    }

    res_q = requests.get(endpoint, headers=getHeader)
    track = res_q.json()
    track = track["tracks"]["items"][0]["external_urls"]["spotify"]

    # 음악 링크 -> 데이터로 바꿔주는 API (Tracks)
    data = track.split("track/")[1].split("?")[0]
    endpoint_f = f"	https://api.spotify.com/v1/audio-features/{data}"
    endpoint_i = f"	https://api.spotify.com/v1/tracks/{data}?market=US"



    res_f = requests.get(endpoint_f, headers=getHeader)
    res_i = requests.get(endpoint_i, headers=getHeader)

    dict_data = {}
    dict_info = {}
    track_features = res_f.json()
    track_info = res_i.json()

    dict_data['danceability'] = track_features['danceability']
    dict_data['acousticness'] = track_features['acousticness']
    dict_data['energy'] = track_features['energy']
    dict_data['key'] = track_features['key']
    dict_data['liveness'] = track_features['liveness']
    dict_data['loudness'] = track_features['loudness']+60
    dict_data['mode'] = track_features['mode']
    dict_data['speechiness'] = track_features['speechiness']
    dict_data['tempo'] = track_features['tempo']
    dict_data['valence'] = track_features['valence']
    dict_data['popularity'] = track_info['popularity']
    df_data = pd.DataFrame([dict_data])


    # dict_info['artist']  = track_info
    dict_info['artist'] = track_info['artists'][0]['name']
    dict_info['image_url'] = track_info['album']['images'][1]['url']
    dict_info['song'] = track_info['name']
    return dict_info, df_data


