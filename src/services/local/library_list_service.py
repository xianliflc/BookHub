from src.libs.config_loader import load_saved_repo_status
from src.libs.objects.local_file_object import (
    LocalFileObject
)
from src.libs.objects.config_object import ConfigObject
from src.libs.local_library import get_existing_downloaded_files

def get_all_downloaded_files(
    config: ConfigObject
) -> list[str]:
    all_files = get_existing_downloaded_files(config)
    return all_files
    
    # file_objects = []
    # file_objects = [
    #     LocalFileObject(
    #         file_name = file[0],
    #         file_path=file[1],
    #     ) for file in all_files
    # ]

    # return file_objects


def get_all_files_from_repos_ststus() -> list[LocalFileObject]:
    repos_status = load_saved_repo_status().repos

    result = []
    for repo in repos_status:
        result += repo.downloaded_files

    return result
