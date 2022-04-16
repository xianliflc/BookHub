import argparse
import hashlib

from src.services.remote.config_service import download_remote_config, output_remote_repo_config
from src.libs.config_loader import (
    load_config, 
)

def main(args):
    config = load_config()
    if args.local:
        pass
    else:
        downloaded_repo = download_remote_config(args.path)
        file_path = output_remote_repo_config(
            downloaded_repo,
            config,
            hashlib.md5(args.path.encode()).hexdigest()
        )
    ### now just downloaded and saved, not added yet
        # print("Repo added", file_path)




if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='libs')
    sub_parsers = parser.add_subparsers(help='libs add help')

    parser_cool = sub_parsers.add_parser('add', help='cools is sub-command with sub-commands')
    parser_cool.add_argument('path', type=str, help='the path to repo config')
    parser_cool.add_argument('--local', '-l', action='store_true')
    parser_cool.add_argument('--tag', '-t', type=str, help='add a tag')

    args = parser.parse_args()

    main(args)