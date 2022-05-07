import argparse
from src.services.local.library_list_service import get_all_files_from_repos_ststus

from src.services.remote.config_service import download_remote_config, output_remote_repo_config
from src.libs.config_loader import (
    load_config,
)

def main(args):
    config = load_config()
    tag = args.tag
    repo = args.repo

    files = get_all_files_from_repos_ststus()

    print(len(files))



if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='libs')
    sub_parsers = parser.add_subparsers(help='libs list help')

    parser_cool = sub_parsers.add_parser('list', help='list all downloaded files')
    parser_cool.add_argument('--tag', '-t', type=str, help='list by a tag')
    parser_cool.add_argument('--repo', '-r', type=str, help='list by a repo name or id')
    args = parser.parse_args()

    main(args)