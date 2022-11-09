from email.header import Header
import json
import requests
import csv
import base64
import time
from screts_key import *
from get_token import getAccessToken


token = getAccessToken(clientID, clientSecret)

def getUserPlaylist(token, user_id):
    """ 
    ### 플레이리스트들을 가져오는 함수
    해당 유저의 플레이리스트 중 MBTI 플레이스트만 가져오는 함수이다.
    - 리턴 값
        - `plist_dicts` : 해당 유저의 다른 플레이리스트 말고 MBTI 플레이리스트의 id만 가져옴
    - 파라미터 값 : `token`, `user_id` (secret.py)
    """

    endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists?limit=30"
    getHeader = {
        "Authorization" : "Bearer " + token
    }

    res_users = requests.get(endpoint, headers=getHeader)
    users_plists = res_users.json() # 유저의 플레이리스트를 json 형식으로 가져옵니다.
    # print(users_plists)

    mbti_list = ['esfp // the entertainer ', 'estp // the rule breaker ', 'isfp // the creative', 'istp // the prodigy ', 'esfj // the authentic ', 'estj // the administrator ', 'isfj // the protector ', 'istj // the logistician ', 'enfp // the individualist ', 'enfj // the protagonist ', 'entp // the debater ', 'entj // the commander ', 'intp // the scholar', 'intj // the architect ', 'infp // the mediator', 'infj // the visionary ']
    plist_titles = []
    plist_dict = {}
    for plist_title in range(0, len(users_plists['items'])):
        mbti_title = users_plists['items'][plist_title]["name"]
        if mbti_title in mbti_list:
            plist_dict[f'{mbti_title}'] = users_plists['items'][plist_title]["id"]
        else :
            pass


    return plist_dict



def getPlisttoTrack(token, playlist_id):
    """
    ### 플레이리스트의 트랙을 가져오는 함수
    해당 플레이리스트에 속한 트랙들을 가져오는 함수이다.
    - 리턴 값
        - `plist_tracks` : 해당 플레이리스트의 트랙들을 가져온다.
    - 파라미터 값 : `token`, `user_id` (secret.py)
    """

    track_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    getHeader = {
        "Authorization" : "Bearer " + token
    }

    res = requests.get(track_endpoint, headers=getHeader)
    plist_tracks = res.json()

    return plist_tracks

# pli_track = {}
# track_dic = {}
 

def gettrackAudioFeatures(token, ids):
    """
    ## 트랙에 대한 정보 가져오기
    해당 트랙에 있는 정보를 가져오는 함수
    - 리턴 값
        - `track_features` : 트랙의 특성을 json 형태로 리턴한다.
    - 파라미터 값 : `token`, `ids` (secret.py)
    """
    endpoint = f"https://api.spotify.com/v1/audio-features?ids={ids}"
    
    getHeader = {
        "Authorization" : "Bearer " + token
    }

    res = requests.get(endpoint, headers=getHeader)
    track_features = res.json()
    
    return track_features


pli_track = {}
track_dic = {}
plist_dicts = getUserPlaylist(token, user_id)

# 추출된 트랙들을 json 파일로 저장한다.
for i in range(0, len(list(plist_dicts.values()))):
    tracks = getPlisttoTrack(token, list(plist_dicts.values())[i]) # tracks : mbti 별 tracks(json)
    for j in range(0, len(tracks['items'])):
        track_dic[j] = {
            'track_id' : tracks['items'][j]['track']['id'],
            'track_name' : tracks['items'][j]['track']['name'],
            'track_artist' : tracks['items'][j]['track']['artists'][0]['name'],  
            'track_image' :  tracks['items'][j]['track']['album']['images'][0]['url'],
            'audio_features' : gettrackAudioFeatures(token, tracks['items'][j]['track']['id'])['audio_features'][0],
            'mbti' : list(plist_dicts.keys())[i].split()[0]
        }

    with open(f'./data/mbti/json/{list(plist_dicts.keys())[i].split()[0]}.json','w') as f: 
        time.sleep(10)
        json.dump(track_dic, f)  
