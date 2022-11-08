from screts_key import *
import json
import requests
import base64

authUrl = "https://accounts.spotify.com/api/token"
authHeader = {}
authData = {}

def getAccessToken(clientID, clientSecret):
    """ 
    ### 클라이언트 자격 증명 토큰을 가져오는 함수
    스포티파이 개발자 홈페이지에서 제공하는 데이터를 가져오기 위해 우선 토큰을 먼저 가져옵니다.
    토큰을 가져오기 서버에 클라이언트 정보와 grant_type을 요청하면 json으로 응답 받으실 수 있습니다.
    - 리턴 값 : `accessToken` 
    - 파라미터 값 : `clientID`, `clientSecert`
    - 참고자료 : https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
    """

    message = f"{clientID}:{clientSecret}" 
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes) # Encoding
    base64_message = base64_bytes.decode('ascii')

    authHeader['Authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"

    res = requests.post(authUrl, headers=authHeader, data=authData) # HTTP Status

    responseObject = res.json()

    accessToken = responseObject['access_token']
    return accessToken

token = getAccessToken(clientID, clientSecret)

def gettitleAudioFeatures(token, title):
    """
    ## 트랙(검색어)을 입력하여 음악적 특성정보  가져오기
    해당 트랙에 있는 정보를 가져오는 함수
    - 리턴 값
        - `info` : id, title, artist, image, url 등 정보를 추출하는 딕셔너리 타입
        - `features` : 음악적 특징을 담아낸 딕셔너리 타입
    - 파라미터 값 : `token`, `title` (secret.py)
    """
    # 검색어로 Track ID 찾기
    endpoint1 = f'https://api.spotify.com/v1/search?q={title}&type=track&include_external=audio&limit=1'
    
    getHeader = {
        "Authorization" : "Bearer " + token
    }

    res = requests.get(endpoint1, headers=getHeader)
    tracks_info = res.json()['tracks']['items'][0]
    track_id = tracks_info['id']
    info = {
        'id' : track_id,
        'title' : tracks_info['name'],
        'artist' : tracks_info['album']['artists'][0]['name'],
        'image' : tracks_info['album']['images'][0]['url'],
        'url' : tracks_info['external_urls']['spotify'] 
    }

    # 트랙 ID를 이용하여 음악적 특징 추출하기
    endpoint2 = f"https://api.spotify.com/v1/audio-features?ids={track_id}"
    res = requests.get(endpoint2, headers=getHeader)
    raw_features = res.json()['audio_features'][0]
    features = {
        'danceability' : raw_features['danceability'],
        'energy' : raw_features['energy'],
        'key' : raw_features['key'],
        'loudness' : raw_features['loudness']+30,
        'mode' : raw_features['mode'],
        'speechiness' : raw_features['speechiness'],
        'acousticness' : raw_features['acousticness'],
        'instrumentalness' : raw_features['instrumentalness'],
        'liveness' : raw_features['liveness'],
        'valence' : raw_features['valence'],
        'tempo' : raw_features['tempo'],
    }
    
    
    return info, features