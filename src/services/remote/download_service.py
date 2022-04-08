from src.libs.objects.remote_repo_object import RemoteRepo
from src.libs.download import download_file_with_target_url_and_local_name
from src.libs.objects.config_object import ConfigObject
from src.libs.config_loader import load_config
from src.vendors.github import Github

def download_file_with_id(
    id: str,
    config: ConfigObject,
    repo: RemoteRepo
):
    download_path = config.download_path
    url = None
    local_file = None
    for file in repo.resource_items:
        if file.id == id:
            url = file.relative_url
            local_file = url.split("/")[-1]
            break
    if not url:
        raise Exception("file id not found in repo")
    print(local_file)
    download_file_with_target_url_and_local_name(
        Github.getRemoteUrl(repo.url, url),
        local_file,
        download_path
    )
