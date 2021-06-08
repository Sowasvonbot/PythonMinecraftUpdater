import json
import sys
import urllib.request as request
from pathlib import Path
from typing import List, Tuple
from urllib.error import URLError

minecraft_url: str = \
    "https://launchermeta.mojang.com/mc/game/version_manifest.json"

script_mode = "snapshot"
script_modes: Tuple[str, str] = ("snapshot", "release")


def get_json_file_from_url(url: str):
    try:
        website_bytes: bytes = request.urlopen(url).read()
        decoded_string = website_bytes.decode("utf-8")
        return json.loads(decoded_string)
    except URLError:
        print(f"Website \"{minecraft_url}\" not reachable\nExiting script!")
        sys.exit(1)


def get_latest_version_url(version_json: dict):
    requested_version = version_json["latest"][script_mode]
    print(
        f"Found version {requested_version} for selected mode: {script_mode}"
    )

    all_versions: List[dict] = version_json["versions"]
    for version in all_versions:
        if version["id"] == requested_version:
            url = version["url"]
    print(f"Found url: {url} for selected version: {requested_version}")

    return url


def extract_server_download_url(version_json: dict):
    url = version_json["downloads"]["server"]["url"]
    return url


def download_source(url: str):
    print("Downloading server.jar")
    download_path = Path(Path(__file__)).parent / "server.jar"
    print(f"Saving to {download_path}")
    request.urlretrieve(url, download_path)
    print("Finished download of server.jar")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] in script_modes:
            script_mode = sys.argv[1]
        else:
            print(f"Please select one of these modes: {script_modes}")
            sys.exit(0)

    json_file = get_json_file_from_url(minecraft_url)
    target_url = get_latest_version_url(json_file)
    json_file = get_json_file_from_url(target_url)
    target_url = extract_server_download_url(json_file)
    download_source(target_url)
