import argparse
import hashlib
from src.libs.local_library import load_downloaded_repo
from src.libs.objects.remote_repo_object import RemoteRepo, RemoteRepos

from src.services.remote.config_service import download_remote_config, output_remote_repo_config
from src.libs.config_loader import (
    build_remote_repos,
    load_config,
    merge_remote_config, 
)

def main(args):
    config = load_config()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='libs')
    sub_parsers = parser.add_subparsers(help='libs list help')

    parser_cool = sub_parsers.add_parser('list', help='list all downloaded files')
    parser_cool.add_argument('--tag', '-t', type=str, help='add a tag')

    args = parser.parse_args()

    main(args)