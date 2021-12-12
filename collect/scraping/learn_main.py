# -*- coding: utf-8 -*-

## 개발자를 위한 Spotify : https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
##  Python의 Base64 인코딩  : https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/

import json
import requests
import base64
from secrets import * # secret.py에서 클라이언트 정보 가져오기

authUrl = "https://accounts.spotify.com/api/token" 
authHeader = {}
authData = {}

# Base64 Encode Client ID and Client Secret

def getAcesssToken(clientID, clientSecret):
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

token = getAcesssToken(clientID, clientSecret)

print(token)

# 이제 토큰을 이용하여 API를 이용할 수 있다.
# https://developer.spotify.com/documentation/web-api/reference/#/

playlist_id = "37i9dQZF1DX4WYpdgoIcn6"
# GET /v1/playlists/playlist_id HTTP/1.1

def getPlaylistTrack(token, playlistID):
    playlistEndPoint = "http://api.spotify.com/v1/playlists/{playlist_id}/1.1"

    getHeader = {
        "Authorization" : "Bearer " + token
    }
    res = requests.get(playlistEndPoint, headers=getHeader)

    playlistObject = res.json()

    return playlistObject

## API Request
token = getAcesssToken(clientID, clientSecret)
playlist_id = "37i9dQZF1DX4WYpdgoIcn6"

tracklist = getPlaylistTrack(token, playlist_id)


# print(json.dumps(tracklist, indent=2))

with open('tracklist.json','w') as f: #json 파일로 저장
    json.dump(tracklist, f)




