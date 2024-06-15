import auth
import requests
import json
import time


def get_query():
    try:
        with open('./scripts/data/bk_albums_raw.json', 'r') as f:
            data = json.load(f)
            artist = data[4]["artist"]
            title = data[4]["title"]
            query = f"{artist} {title}"
            return query
    except FileNotFoundError:
        print("File not found")


def search_for_item(query):
    token_info = auth.load_token_info()
    if auth.is_token_expired(token_info):
        print("Token is expired, fetching a new one...")
        token_info = auth.get_access_token()
    else:
        print("Token is still valid.")

    search_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token_info['access_token']}"
    }

    params = {
        "q": query,
        "type": "album",
        "limit": 1
    }

    time.sleep(2.0)

    response = requests.get(search_url, headers=headers, params=params).json()
    album_id = response['albums']['items'][0]['id']
    return album_id


if __name__ == "__main__":
    query = get_query()
    print("***************get_query called****************")
    album_id = search_for_item(query)
