import requests
import os
import json
from typing import List


def get_albums(api_key: str, shared=False):
    """get_albums Get all albums owned by the api_key owner

    Args:
        api_key (str): API key of an Immich user
        shared (bool, optional): Include shared albums. Defaults to False.

    Returns:
        List of albums
    """
    headers = {"Accept": "application/json", "x-api-key": api_key}

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums'
    if shared:
        url += f"?shared=true"
    response = requests.request("GET", url, headers=headers)
    res = response.json()
    return res


def get_album_info(api_key: str, album_id: str):
    """get_album_info Get details of an album

    Args:
        api_key (str):  API key of an Immich user
        album_id (str): ID of album to get

    Returns:
        Album info
    """
    headers = {"Accept": "application/json", "x-api-key": api_key}

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums/{album_id}'
    response = requests.request("GET", url, headers=headers)
    return response.json()


def create_album(api_key: str, album_name: str):
    """create_album Create a new album for a user

    Args:
        api_key (str):  API key of an Immich user
        album_name (str): Name of new album to create

    Returns:
        Info about the newly created album
    """
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
    """add_assets_to_album Add a list of assets (photos, videos) to an album

    Args:
        api_key (str):  API key of an Immich user
        album_id (str): ID of album to add assets to
        assets (list[str]): ID list of assets to add
    """
    payload = {"ids": assets}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums/{album_id}/assets'
    requests.request("PUT", url, headers=headers, data=json.dumps(payload))


def remove_assets_from_album(api_key: str, album_id: str, assets: "list[str]"):
    """remove_assets_from_album Remove assets from an album

    Args:
        api_key (str): API key of an Immich user
        album_id (str): ID of album to remove assets from
        assets (list[str]): ID list of assets to remove
    """
    payload = {"ids": assets}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums/{album_id}/assets'
    requests.request("DELETE", url, headers=headers, data=json.dumps(payload))


def add_users_to_album(api_key: str, album_id: str, user: str, role: str):
    """add_users_to_album Share an album to user with a given role

    Args:
        api_key (str): API key of an Immich user
        album_id (str): ID of album to share
        user (str): Username of target user
        role (str): Role to grant user
    """
    payload = {"albumUsers": [{"userId": user, "role": role}]}

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums/{album_id}/users'
    requests.request("PUT", url, headers=headers, data=json.dumps(payload))


def delete_album(api_key: str, album_id: str):
    """delete_album Delete an album

    Args:
        api_key (str): API key of an Immich user
        album_id (str): ID of album to delete
    """
    url = f'{os.environ["IMMICH_BASE_URL"]}/api/albums/{album_id}'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    res = requests.request("DELETE", url, headers=headers)

def delete_assets(api_key: str, ids: List[str]):
    """delete_assets Fully delete an asset (bypassing trash)
    Asset must be owned by user.

    Args:
        api_key (str): API key of an Immich user
        ids (List[str]): ID list of assets to delete.
    """
    payload = {
        "force": True,
        "ids": ids
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    url = f'{os.environ["IMMICH_BASE_URL"]}/api/assets'
    requests.request("DELETE", url, headers=headers, data=json.dumps(payload))