import json
import os

from src.libs.objects.remote_repo_object import RemoteRepo

DOWNLOAD_REPO_DIR = '..\\..\\output\\'

def get_downloaded_files(
    file_path: str
) -> list[str]:

    listOfFiles = list()
    for (dirpath, _, filenames) in os.walk(file_path):
        listOfFiles += [[file, os.path.join(dirpath, file)] for file in filenames]

    return listOfFiles

def load_downloaded_repo(file_path: str) -> dict:
    filename = os.path.join(file_path)
    f = open(filename)
    data = json.load(f)
    f.close()

    return data