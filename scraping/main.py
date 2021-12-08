# -*- coding: utf-8 -*-

"""
Spotify API Token을 불러오는 작업

Reference
- 개발자를 위한 Spotify : https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
- Python의 Base64 인코딩 : https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/

1. Get Access Token : Ascii 코드를 Base64인코딩하는 작업
"""

import json
import requests
import base64
from secrets import *

from requests.api import head # secret.py에서 클라이언트 정보 가져오기

authUrl = "https://accounts.spotify.com/api/token"
authHeader = {}
authData = {}

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

# print(token)
# access_token = ??

"""
## Find Tracks Audio Functions
Link  : https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features

"""

# def getTrackFunctions(token, id):
#     endpoint = f"http://api.spotify.com/v1/audio-features/{id}"

#     getHeader = {
#         "Authorization" : "Bearer " + token
#     }
#     res = requests.get(endpoint, headers=getHeader)

#     trackinfo = res.json()

#     return trackinfo

# id = "2g0LdZQce9xlcHb1mBJyuz"
# trackInfo = getTrackFunctions(token, id)

# with open('trackinfo.json','w') as f: #json 파일로 저장
#     json.dump(trackInfo, f)


# -------------------------------------

user_id = "annieboyse"

# User의 Playlist 불러오는 API 함수
def getUserPlaylist(token, user_id): 
    """
    ## 플레이리스트를 가져오는 함수
    1. MBTI Playlist를 정리해놓은 사용자의 플레이리스트를 API를 활용해서 불러온다.
    2. `{Title : ID}` 형식으로 `plist_dict`을 리턴한다.
    3. API를 활용한 원본 json 형식을 `users_plists`으로 리턴한다.

    """
    endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    getHeader = {
      "Authorization" : "Bearer " + token
       }
    
    res_users = requests.get(endpoint, headers=getHeader)
    users_plists = res_users.json()

    # Playlist Title을 리스트로 만든다음,
    plist_titles = []
    for plist_title in range(0, len(users_plists['items'])) : # 3번째 플레이리스트부터 MBTI 플레이리스트 이기 때문에 이전 index는 뺐습니다.
        plist_titles.append(users_plists['items'][plist_title]["name"])

    # print(plist_titles)

    # Dictionary 형태로 Playlist를 제목 : id 순으로 정리하고 Json 파일로 저장하였습니다.
    plist_dict = {}
    for i in range(0, len(plist_titles)) :
        plist_dict[f'{plist_titles[i]}'] = users_plists['items'][i]["id"]

    del plist_dict['saturday morning baking <33']
    del plist_dict['riot grrrl ']
    del plist_dict['happy brain chemicals go brrr ']
    del plist_dict['armin\'s playlist']

    return plist_dict, users_plists

plist_dicts, users_plists  = getUserPlaylist(token, user_id)

with open(f'./json_data/MBTI_plist1.json','w') as f:
    json.dump(plist_dicts, f)


# Playlist의 Tracks를 가져오는 함수를 지정하였습니다.
def getPlaylistTracks(token, playlist_id):
    """
    ## playlist의 트랙들을 가져오는 함수
    1. MBTI별 각기 다른 플레이리스트에서 트랙들을  가져온다.
    2. json 변수인 `playlist_track`에서 for문을 이용하여 MBTI 별로 분류한다.
    3. 분류된 플레이리스트에서 `{num : Track_id}`로 json 파일을 피클링 한다.
    """
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    getHeader = {
        "Authorization" : "Bearer " + token
    }

    res = requests.get(endpoint, headers=getHeader)
    playlist_track = res.json()

    return playlist_track

track_dic = {}

for i in range(0, len(list(plist_dicts.values()))):
    tracks = getPlaylistTracks(token, list(plist_dicts.values())[i]) # 위 함수를 이용하여 `tracks`에 저장한다.
    for j in range(0, len(tracks['items'])): # MBTI 별 트랙에서 `{순서 : track_id}` 순으로 json 피클링을 한다.
        track_dic[f'{j}'] = tracks['items'][j]['track']['id']
    # with open(f'./json_data/mbti_track/{list(plist_dicts.keys())[i].split()[0]}.json','w') as f:
    #     json.dump(track_dic, f)

print(track_dic.values())
