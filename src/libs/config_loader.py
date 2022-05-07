from datetime import datetime
import json
import os
from time import strftime
from src.libs.objects.local_file_object import LocalFileObject
from src.libs.objects.remote_repo_object import  (
    RemoteItemObject, RemoteRepo, RemoteRepos)
from src.libs.objects.config_object import ConfigObject
from src.libs.objects.saved_repo_status import RepoStatus, ReposStatus

REMOTE_LIBRARY_SETTING_PATH = '..\\..\\configs\\remote_library_settings.json'
LOCAL_SETTING_PATH = '..\\..\\configs\\local_settings.json'
SAVED_REPO_STATUS = '..\\..\\configs\\saved_remote_repo_status.json'
DATE_TIME_FORMAT = '%Y-%m-%d, %H:%M:%S'

def load_config() -> ConfigObject:
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, LOCAL_SETTING_PATH)
    f = open(filename)
    data = json.load(f)

    config = ConfigObject(data['user_setting'], data['system_setting'])
    f.close()
    return config

def load_remote_config() -> RemoteRepos:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, REMOTE_LIBRARY_SETTING_PATH)
    
    try:
        f = open(filename)
        data = json.load(f)

        f.close()
    except Exception:
        return build_remote_repos([])

    return build_remote_repos(data['repos'])

def load_saved_repo_status() -> ReposStatus:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, SAVED_REPO_STATUS)
    
    try:
        f = open(filename)
        data = json.load(f)

        f.close()
    except Exception:
        return build_saved_remote_repo_status([])
    return build_saved_remote_repo_status(data['repos'])

def build_saved_remote_repo_status(data: list) -> ReposStatus:
    repos = []
    for re in data:
        items = []
        for item in re['downloaded_files']:
            items.append(
                LocalFileObject(
                    path = item['path'],
                    id = item['id'],
                    created_at = datetime.strptime(item['created_at'], DATE_TIME_FORMAT),
                    updated_at =  datetime.strptime(item['updated_at'], DATE_TIME_FORMAT),
                    opened_at =  datetime.strptime(item['opened_at'], DATE_TIME_FORMAT) if item['opened_at'] else None
                )
            )

        repo = RepoStatus(
            name=re['name'],
            md5=re['md5'],
            updated_at=datetime.strptime(re['updated_at'], DATE_TIME_FORMAT),
            created_from=re['created_from'],
            created_at=datetime.strptime(re['created_at'], DATE_TIME_FORMAT),
            updates_detected_at=datetime.strptime(re['updates_detected_at'], DATE_TIME_FORMAT) if re['updates_detected_at'] else None,
            has_updates=re['has_updates'],
            is_archieved=re['is_archieved'],
            downloaded_files=items
        )
        repos.append(repo)
    config = ReposStatus(repos)
    return config

def build_remote_repos(data: list):
    repos = []
    for re in data:
        items = []
        for item in re['resource_items']:
            obj = RemoteItemObject(
                    resource_item_name=item['resource_item_name'],
                    author=item['author'],
                    resource_type=item['resource_type'],
                    relative_url=item['relative_url'],
                    description=item['description'],
                )
            if 'id' not in item:
                obj.initialize()
            else:
                obj.id = item['id']
            items.append(obj)

        repo = RemoteRepo(
            name=re['name'],
            resource_vendor=re['resource_vendor'],
            url=re['url'],
            resource_items=items,
            version=re['version'],
            maintainer=re['maintainer'],
            tags=re['tags'],
            description=re['description']
        )
        repo.id = re.get('id', None) 
        repos.append(repo)
    config = RemoteRepos(repos)
    return config

def init_remote_configs(
    repos:RemoteRepos,
    force: bool = False
) -> RemoteRepos:
    has_updates = False
    for k in range(len(repos.repos)):
        if force or not repos.repos[k].is_initialized:
            repos.repos[k].initialize()
            has_updates = True

    if has_updates:
        save_remote_configs(repos)
    return repos

def save_remote_configs(
    config:RemoteRepos
) -> None:
    configs = {'repos': []}
    repos = config.repos
    for k in range(len(repos)):
        repo = repos[k].__dict__.items()
        repo_dict = {}
        for k,v in repo:
            if k != 'resource_items':
                repo_dict[k] = v
            else:
                the_list_obj = []
                for item in v:
                    the_list_obj.append(item.__dict__)
                repo_dict[k] = the_list_obj
        configs['repos'].append(repo_dict)

    json_object = json.dumps(configs, indent = 4)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, REMOTE_LIBRARY_SETTING_PATH)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def save_repos_status(repos_status: ReposStatus):
    configs = {'repos': []}
    repos = repos_status.repos
    for k in range(len(repos)):
        repo = repos[k].__dict__.items()
        repo_dict = {}
        
        for k,v in repo:
            if k != 'downloaded_files':
                if k == 'created_at':
                    repo_dict[k] = v.strftime(DATE_TIME_FORMAT)
                elif k == 'updated_at':
                    repo_dict[k] = v.strftime(DATE_TIME_FORMAT)
                elif k == 'updates_detected_at' and v:
                    repo_dict[k] = v.strftime(DATE_TIME_FORMAT)
                else:
                    repo_dict[k] = v
            else:
                the_list_obj = []
                for item in v:
                    if item.created_at:
                        item.created_at = item.created_at.strftime(DATE_TIME_FORMAT)
                    if item.updated_at:
                        item.updated_at = item.updated_at.strftime(DATE_TIME_FORMAT)
                    if item.opened_at:
                        item.opened_at = item.opened_at.strftime(DATE_TIME_FORMAT)
                    the_list_obj.append(item.__dict__)
                repo_dict[k] = the_list_obj

        configs['repos'].append(repo_dict)
        

    json_object = json.dumps(configs, indent = 4)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, SAVED_REPO_STATUS)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def save_local_config(
    config: ConfigObject
) -> None:
    config_dict = {'user_setting': {}, 'system_setting': {}}
    if config.user:
        config_dict['user_setting'] = config.user
    if config.system:
        config_dict['system_setting'] = config.system

    json_object = json.dumps(config_dict, indent = 4)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, LOCAL_SETTING_PATH)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def merge_repo_status(
    repos: list[RemoteRepo],
    repos_status: ReposStatus
):
    for repo in repos:
        repo_status = RepoStatus(
            name=repo.name,
            md5=repo.id,
            created_from='remote', #TODO: add logic local or remote
            updated_at=datetime.now(),
            created_at=datetime.now(),
            updates_detected_at=None,
            has_updates=None,
            is_archieved=False,
            downloaded_files=[]
        )
        repos_status.repos.append(repo_status)

    return repos_status
    

def merge_remote_config(
    new_remote_repos: RemoteRepos
) -> tuple[int, list[str]]:
    if not new_remote_repos.repos:
        return 0
    
    existing_repos = load_remote_config()
    existing_repos_status = load_saved_repo_status()
    initialized_new_repos = init_remote_configs(new_remote_repos, True)
    existing_md5s = [item.id for item in existing_repos.repos]    
    merging_repos = []
    messages = []
    for repo in initialized_new_repos.repos:
        if repo.id in existing_md5s:
            messages.append(f"{repo.name } already exists.")
            continue
        merging_repos.append(repo)
    existing_repos.repos += merging_repos
    save_remote_configs(existing_repos)
    existing_repos_status = merge_repo_status(merging_repos, existing_repos_status)
    save_repos_status(existing_repos_status)
    return (len(merging_repos), messages)

def write_to_file(
    str_to_file: str,
    file_name: str,
    directory: str
) -> bool:
    if not os.path.exists(directory):
            access = 0o777
            os.makedirs(directory, access)
    file_path = os.path.join(directory, file_name)
    with open(file_path, "w") as outfile:
        outfile.write(str_to_file)
        return True