import psycopg2 as pg
import immich
from psycopg2.extras import RealDictCursor
import json
import os
import argparse

parser = argparse.ArgumentParser(
                    prog='Immich Tools',
                    description='Helpful tools for immich')

parser.add_argument('mode', choices=["create-album", "delete-images"])                    

args = parser.parse_args()


conn = pg.connect(
    database=os.environ["IMMICH_DB"],
    user=os.environ["IMMICH_DB_USER"],
    password=os.environ["IMMICH_DB_PASSWORD"],
    host=os.environ["IMMICH_DB_HOST"],
)

conn.set_client_encoding("UTF8")
cursor = conn.cursor(cursor_factory=RealDictCursor)

def create_album():
    with open('data.json') as json_data:
        data = json.load(json_data)

    cursor.execute("SELECT * FROM public.user;")
    users = cursor.fetchall()

    def user_to_id(user: str):
        return next(u["id"] for u in users if u["email"] == user)

    class AlbumMappings:
        def __init__(
            self, owner_api_key: str, base_path: str, shared_to: "dict[str, str]"
        ) -> None:
            self.owner_api_key = owner_api_key
            self.base_path = base_path
            self.shared_to = shared_to

    album_mappings = [AlbumMappings(os.environ[d['key_name']], d['base_path'], d['users']) for d in data['album_mappings']]

    for am in album_mappings:
        albums = immich.get_albums(am.owner_api_key)
        albums = { album['albumName']: album for album in albums }
        # Get all the folders under the base path
        for album in os.listdir(am.base_path):
            print("Processing: ", album)
            if album not in albums:
                print(f"Album {album} not found. Creating new album.")
                print(albums)
                albums[album] = immich.create_album(am.owner_api_key, album)

            album_id = albums[album]["id"]

            for user, role in am.shared_to.items():
                immich.add_users_to_album(
                    am.owner_api_key, album_id, user_to_id(data['user_map'][user]), role
                )

            album_album_info = immich.get_album_info(am.owner_api_key, album_id)
            found_files = []
            path = os.path.join(am.base_path, album)
            for dirpath, subdirs, files in os.walk(path):
                found_files.extend([os.path.join(dirpath, x) for x in files])

            # Get a set of files without the extensions
            file_set = {'.'.join(f.lower().split('.')[0:-1]) for f in found_files if f.lower().split('.')[-1] != 'mov'}
            # if the set size is different from the total file count, then there are duplicate names without extensions.
            # which means there's probaby live photos. We should only add the image portion of the live photo to the album and not the video portion.
            # For handling bug https://github.com/immich-app/immich/issues/2665
            if (len(file_set) != len(found_files)):
                clean_files = []
                for file in found_files:
                    file_split = file.lower().split('.')
                    if file_split[-1] == 'mov' or file_split[-1] == 'mp4':
                        if '.'.join(file_split[0:-1]) in file_set:
                            print("live photo video", '.'.join(file_split[0:-1]))
                            continue
                    clean_files.append(file)

                
                found_files = clean_files

            cursor.execute(
                cursor.mogrify(
                    'SELECT "originalPath", "id" FROM asset where "originalPath" = ANY(%s);',
                    [found_files],
                )
            )
            file_id_maps = {v["originalPath"]: v["id"] for v in cursor.fetchall()}

            cursor.execute(
                'SELECT "assetsId" FROM album_asset WHERE "albumsId" = %s',
                [album_id],
            )

            online_images = set(map(lambda i: i["assetsId"], cursor.fetchall()))
            images = {file_id_maps[k] for k in file_id_maps}
            # images that are present in the album  that should be removed
            deleted_images = list(online_images.difference(images))
            # images that are missing from the album that need to be added
            new_images = list(images.difference((online_images)))

            print("Adding images to album: ", len(new_images))
            for i in range(0, len(new_images), 100):
                immich.add_assets_to_album(
                    am.owner_api_key, album_id, new_images[i : i + 100]
                )

            print("Deleting images from album: ", len(deleted_images))
            for i in range(0, len(deleted_images), 100):
                immich.remove_assets_from_album(
                    am.owner_api_key, album_id, deleted_images[i : i + 100]
                )


def delete_images():
    for account in os.environ["SHARED_ACCOUNTS"].split(','):
        account_key = os.environ[account]
        albums = immich.get_albums(account_key, True)
        delete_albums = filter(lambda a: a['albumName'] == "delete", albums)

        for album in delete_albums:
            info = immich.get_album_info(account_key, album['id'])
            images = info['assets']
            image_ids = [i['id'] for i in images]
            immich.delete_assets(account_key, image_ids)
            print(f'Deleted: {len(image_ids)} for {account}')
        
match args.mode:
    case "create-album":
        create_album()
    case "delete-images":
        delete_images()