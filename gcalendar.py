import time
import jwt
import json
import requests

def get_signed_jwt(token_json):
    private_key_id = token_json.get("private_key_id")
    private_key = token_json.get("private_key")

    iat = time.time()
    exp = iat + 3600
    payload = {
        'iss': token_json.get("client_email"),
        'scope': 'https://www.googleapis.com/auth/calendar.readonly',
        'aud': token_json.get("token_uri"),
        'iat': iat,
        'exp': exp
    }
    additional_headers = {'kid': private_key_id} 
    signed_jwt = jwt.encode(payload, private_key, headers=additional_headers,algorithm='RS256') 
    return signed_jwt

def get_access_token():
    token_json = json.load(open("env/token.json"))
    jwt = get_signed_jwt(token_json)
    response = requests.post(
        token_json.get("token_uri"),
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': jwt
        }
    )
    response.raise_for_status()
    return response.json()['access_token']

if __name__ == '__main__':
    access_token = get_access_token()
    calendar_id = "june.333@humanscape.io"
    curtime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(time.time()))
    URL = 'https://www.googleapis.com/calendar/v3/calendars/'+calendar_id +'/events'+'?timeMin='+curtime
    request_header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
        "X-GFE-SSL": "yes"
    }
    response = requests.get(URL, headers=request_header)

    for event in response.json().get("items"):
        print(f'{event.get("summary")} {event.get("start").get("dateTime")} {event.get("end").get("dateTime")}')