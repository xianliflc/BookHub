from src.libs.objects.local_file_object import (
    LocalFileObject
)
from src.libs.objects.config_object import ConfigObject
from src.libs.local_library import get_downloaded_files

def get_all_downloaded_files(
    config: ConfigObject
) -> list[LocalFileObject]:
    file_path = config.system['download_path']
    all_files = get_downloaded_files(file_path)

    file_objects = []
    file_objects = [
        LocalFileObject(
            file_name = file[0],
            file_path=file[1],
        ) for file in all_files
    ]

    return file_objects