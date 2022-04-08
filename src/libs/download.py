import requests
import logging
import os


def download_file_with_target_url_and_local_name(
    remote_url: str,
    local_file: str,
    directory: str
) -> None:
    try: 
        data = requests.get(remote_url)
        file_path = os.path.join(directory, local_file)
        print(file_path)
        if not os.path.exists(directory):
            access = 0o777
            os.makedirs(directory, access)
        with open(file_path, 'wb')as file:
            file.write(data.content)
    except Exception as e:
        print('------------------------------')
        print(e)
        print('------------------------------')


def load_remote_config_file(
    remote_url: str
):
    data = None
    try:
        if remote_url.split('.')[-1] != 'bh':
            print('WARNING: the remote repo config may not be supported')
        data = requests.get(remote_url)
        if data.status_code != 200:
            raise Exception('ERROR: download file')
    except Exception as e:
        print('------------------------------')
        print(e)
        print('------------------------------')

    return data.content.decode('utf-8')