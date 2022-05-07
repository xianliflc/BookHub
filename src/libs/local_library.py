import json
import os
from src.libs.objects.config_object import ConfigObject

from src.libs.objects.remote_repo_object import RemoteRepo


def get_existing_downloaded_files(
    config: ConfigObject
) -> list[str]:

    listOfFiles = list()
    for (dirpath, _, filenames) in os.walk(config.download_path):
        listOfFiles += [[file, os.path.join(dirpath, file)] for file in filenames]

    return listOfFiles

def load_downloaded_repo(file_path: str) -> dict:
    filename = os.path.join(file_path)
    f = open(filename)
    data = json.load(f)
    f.close()

    return data