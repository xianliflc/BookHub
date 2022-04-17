import json
import os
from src.libs.objects.remote_repo_object import  (
    RemoteItemObject, RemoteRepo, RemoteRepos)
from src.libs.objects.config_object import ConfigObject

REMOTE_LIBRARY_SETTING_PATH = '..\\..\\configs\\remote_library_settings.json'
LOCAL_SETTING_PATH = '..\\..\\configs\\local_settings.json'

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
    f = open(filename)
    data = json.load(f)

    f.close()

    return build_remote_repos(data['repos'])


def build_remote_repos(data: dict):
    repos = []
    for re in data:
        items = []
        for item in re['resource_items']:
            items.append(
                RemoteItemObject(
                    resource_item_name=item['resource_item_name'],
                    author=item['author'],
                    resource_type=item['resource_type'],
                    relative_url=item['relative_url'],
                    description=item['description']
                )
            )

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

def merge_remote_config(
    new_remote_repos: RemoteRepos
) -> tuple[int, list[str]]:
    if not new_remote_repos.repos:
        return 0
    
    existing_repos = load_remote_config()
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