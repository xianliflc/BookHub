from datetime import datetime
from src.libs.objects.local_file_object import LocalFileObject
from src.libs.objects.remote_item_object import RemoteItemObject
from src.libs.objects.remote_repo_object import RemoteRepo, RemoteRepos
from src.libs.download import download_file_with_target_url_and_local_name
from src.libs.objects.config_object import ConfigObject
from src.libs.config_loader import load_config, load_saved_repo_status, save_repos_status
from src.libs.objects.saved_repo_status import RepoStatus, ReposStatus
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
    download_file_with_target_url_and_local_name(
        Github.getRemoteUrl(repo.url, url),
        local_file,
        download_path
    )

def search_file_by_name_or_id(
    file_name_or_id: str,
    remote_repos: RemoteRepos,
    repo_name_or_id: str = None
):
    result = []
    for repo in remote_repos.repos:
        if repo_name_or_id and repo.name != repo_name_or_id:
            continue
        if repo_name_or_id and repo.id != repo_name_or_id:
            continue
        items = {item.resource_item_name: item for item in repo.resource_items}
        item_ids = {item.id: item for item in repo.resource_items}
        if file_name_or_id in items:
            result.append({'repo': repo, 'file': items[file_name_or_id]})
            continue
        if file_name_or_id in item_ids:
            result.append({'repo': repo, 'file': item_ids[file_name_or_id]})
            continue
    return result

    
def download_file(
    item_object: RemoteItemObject,
    repo: RemoteRepo,
    config: ConfigObject
):
    download_path = config.download_path
    url = item_object.relative_url
    local_file = url.split("/")[-1]
    if not url:
        raise Exception("file id not found in repo")
    return download_file_with_target_url_and_local_name(
        Github.getRemoteUrl(repo.url, url),
        local_file,
        download_path
    )

def update_repo_status_after_download(
    item_object: RemoteItemObject,
    repo_status: RepoStatus,
    file_path: str
):
    time_now = datetime.now()
    repo_status.updated_at = time_now

    for i in range(len(repo_status.downloaded_files)):
        if repo_status.downloaded_files[i].id == item_object.id:
            repo_status.downloaded_files[i].updated_at = time_now
            repo_status.downloaded_files[i].path = file_path
            return repo_status

    repo_status.downloaded_files.append(
        LocalFileObject(
            path=file_path,
            id=item_object.id,
            created_at=time_now,
            updated_at=time_now
        )
    )
    return repo_status


def download_files_and_update_repo_status(
    items: list[dict],
    config: ConfigObject
):
    repos_status = load_saved_repo_status()

    for item in items:
        file_path = download_file(
            item_object=item['file'],
            repo=item['repo'],
            config=config
        )
        for i in range(len(repos_status.repos)):
            if repos_status.repos[i].md5 == item['repo'].id:
                repos_status.repos[i] = update_repo_status_after_download(
                    item['file'],
                    repos_status.repos[i],
                    file_path
                )
                break    

    save_repos_status(repos_status)