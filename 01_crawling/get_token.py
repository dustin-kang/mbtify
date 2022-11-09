from screts_key import *
from requests.api import head

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

    import json
    import requests
    import base64

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