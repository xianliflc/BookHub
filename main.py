# from src.services.remote.download_service import download_file_with_name

# download_file_with_name()
from src.libs.config_loader import (
    load_config, load_remote_config, init_remote_configs,
    save_local_config
)
from src.services.remote.download_service import download_file_with_id
from src.services.remote.config_service import create_and_output_remote_repo_config

config = load_config()
# remote_repos = load_remote_config()
# remote_repos = init_remote_configs(remote_repos, True)
# for item in remote_repos.repos:
#     print(item.id)
#     for i in item.resource_items:
#         print(i.id)
#         download_file_with_id(
#             i.id
#             , config, remote_repos.repos[0])

# config.user['tags'].append(["tag1", 'tag2'])
# save_local_config(config)

from src.services.local.library_list_service import get_all_downloaded_files
all_files = get_all_downloaded_files(config)
for item in all_files:
    # print(item.__dict__)
    pass


data = {
    "name": "asdasd",
    "resource_vendor": "",
    "url": "http://localhost",
    "description": "",
    "tags" : [],
    "version" : 1,
    "maintainer": "sad",
    "resource_items": [
    ]
}
create_and_output_remote_repo_config(
    data, config, 'test1'
)

