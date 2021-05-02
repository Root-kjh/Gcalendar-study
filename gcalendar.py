import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.oauth2 import id_token
from google_auth_oauthlib.flow import InstalledAppFlow
import time
import requests

if __name__ == '__main__':
    access_token = "AIzaSyDGRXC6hBvdf7ZsFYFhyPv9Z779ZMlgJOg"
    calendar_id = "june.333@humanscape.io"
    curtime = time.strftime('%Y-%m-%dT00:00:00-0000', time.localtime(time.time()))
    URL = 'https://www.googleapis.com/calendar/v3/calendars/'+calendar_id +'/events'+'?timeMin='+curtime
    request_header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
        "X-GFE-SSL": "yes"
    }
    response = requests.get(URL, headers=request_header)

    print(response.text)