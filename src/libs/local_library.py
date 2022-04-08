import os

def get_downloaded_files(
    file_path: str
) -> list[str]:

    listOfFiles = list()
    for (dirpath, _, filenames) in os.walk(file_path):
        listOfFiles += [[file, os.path.join(dirpath, file)] for file in filenames]

    return listOfFiles