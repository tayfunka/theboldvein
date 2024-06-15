import requests
import time
import json
import os

CLIENT_ID = "2b6dad33842a4764bcb8a539b4165d09"
CLIENT_SECRET = "760ae141fb674aa788563451a4f10a17"
TOKEN_FILE = "token_info.json"


def save_token_info(token_info):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_info, f)


def load_token_info():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    else:
        print("Token not found, fetching new token...")
        token_info = get_access_token()
        save_token_info(token_info)
        return token_info


def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(url=url, headers=headers, data=data).json()
    access_token = response['access_token']
    expires_in = response['expires_in']
    expires_at = int(time.time()) + expires_in
    token_info = {
        "access_token": access_token,
        "expires_at": expires_at
    }

    save_token_info(token_info)
    return token_info


def is_token_expired(token_info):
    now = int(time.time())
    return token_info["expires_at"] - now < 60
