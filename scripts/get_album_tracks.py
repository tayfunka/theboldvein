import auth
import time
import requests
import logging
import search_for_item


def get_album_tracks(id):
    token_info = auth.load_token_info()
    if auth.is_token_expired(token_info):
        print("Token is expired, fetching a new one...")
        token_info = auth.get_access_token()
    else:
        print("Token is still valid.")

    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {
        "Authorization": f"Bearer {token_info['access_token']}"
    }

    time.sleep(2.0)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        album_tracks = response.json().get('items', [])
        print(response.json())
        track_ids = [track["id"] for track in album_tracks]
        print(track_ids)
        return track_ids

    except requests.RequestException as e:
        logging.error(f"Error during Spotify API request: {e}")
        return None


if __name__ == "__main__":
    query = search_for_item.get_query()
    album_id = search_for_item.search_for_item(query)
    if album_id:
        result = get_album_tracks(album_id)
