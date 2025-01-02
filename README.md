# Immich Album Sync
This is a python tool that automatically creates Immich albums based on folder structure of an external library.

This takes inspiration from https://gist.github.com/davidacampos/47138edcdc3ac040c05e8f3d6f6a9224, but with a few new features

* Takes into consideration live photos/motion images and only adds the image portion of the image/video pair to the album.
* Look into subdirectories of the base path.
* Run against multiple base paths.
* Handle shared/album by automatically granting permissions based on base paths.
* A bit more performant by connecting directly to the database do the search for images, rather than loading all assets into the script through the rest API.

This tool will NOT do the following
* Delete existing albums. However, it will modify and delete images in an album if it matches the same name as a folder in your base path, and add new photos to it. This also means the script can be run multiple times with the same results, and will not do busy work.


# How the folder structure translates to albums
```
base
 - album1
   - sub_folder1
     - photo1
     - photo2
   - sub_folder2
     - photo3
     - photo4
 - album2
   - photo5
   - photo6
```
photos 1~4 will all be in album1, and photos 5~6 will be in album2.


# Usage
Copy `data.json.example` to `data.json` and replace values
Copy `.env.example` to `.env` and replace values
Update the volume in `docker-compose`. The `/data` is where you have your image library. The path that the script sees must match the same path Immich sees, as it uses the path to query in the database.

Execute `docker-compose up` (or `docker compose up` if you have compose v2) (replace with podman as needed, you don't need instructions for podman if you're using it)

# File explanation
* `user_map` : A friendly name that will be used to reference a user in album mappings, mapped to an email that the user uses in Immich. The name is only used in the script, and is not related to Immich's name for said user.
* `album_mapping` : A list of paths that will be looked against. 
  * key_name: The key created in .env of the user that will own the album. 
  * base_path:  Where the script will go in to look for images.
  * users: An optional list of users that will have additional permissions in the album. Useful for creating shared albums

# To do
Add ability to exclude folders in a path.