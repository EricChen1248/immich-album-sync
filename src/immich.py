import requests
import os
import json


def get_albums(api_key):
    headers = {"Accept": "application/json", "x-api-key": api_key}

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums'
    response = requests.request("GET", url, headers=headers)
    albums = {}
    res = response.json()
    for album in res:
        print(album)
        albums[album["albumName"]] = album
    return albums


def get_album_info(api_key: str, album_id: str):
    headers = {"Accept": "application/json", "x-api-key": api_key}

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums/{album_id}'
    response = requests.request("GET", url, headers=headers)
    return response.json()


def create_album(api_key, album_name):
    payload = {"albumName": album_name}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }
    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums'
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return response.json()


def add_assets_to_album(api_key: str, album_id: str, assets: "list[str]"):
    payload = {"ids": assets}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums/{album_id}/assets'
    requests.request("PUT", url, headers=headers, data=json.dumps(payload))


def remove_assets_from_album(api_key: str, album_id: str, assets: "list[str]"):
    payload = {"ids": assets}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums/{album_id}/assets'
    requests.request("DELETE", url, headers=headers, data=json.dumps(payload))


def add_users_to_album(api_key: str, album_id: str, user: str, role: str):
    payload = {"albumUsers": [{"userId": user, "role": role}]}

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums/{album_id}/users'
    requests.request("PUT", url, headers=headers, data=json.dumps(payload))
