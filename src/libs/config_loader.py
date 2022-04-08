import json
import os
from src.libs.objects.remote_repo_object import  (
    RemoteItemObject, RemoteRepo, RemoteRepos)
from src.libs.objects.config_object import ConfigObject
 

def load_config() -> ConfigObject:
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '..\\..\\configs\\local_settings.json')
    f = open(filename)
    data = json.load(f)
    config = ConfigObject(data['user_setting'], data['system_setting'])
    f.close()
    return config

def load_remote_config() -> RemoteRepos:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '..\\..\\configs\\remote_library_settings.json')
    f = open(filename)
    data = json.load(f)
    repos = []
    for re in data['repos']:
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
        repos.append(
            RemoteRepo(
                name=re['name'],
                resource_vendor=re['resource_vendor'],
                url=re['url'],
                resource_items=items,
                version=re['version'],
                maintainer=re['maintainer'],
                tags=re['tags'],
                description=re['description']
            )
        )
    config = RemoteRepos(repos)
    f.close()

    return config


def init_remote_configs(
    config:RemoteRepos,
    force: bool = False
) -> None:
    has_updates = False
    for k in range(len(config.repos)):
        if force or config.repos[k].is_initialized:
            config.repos[k].initialize()
            has_updates = True

    if has_updates:
        save_remote_configs(config)
    return config

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
    filename = os.path.join(dirname, '..\\..\\configs\\remote_library_settings.json')
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
    filename = os.path.join(dirname, '..\\..\\configs\\local_settings.json')
    with open(filename, "w") as outfile:
        outfile.write(json_object)


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