import argparse
from src.libs.config_loader import (
    load_config,
    load_remote_config,
)
from src.services.remote.download_service import download_files_and_update_repo_status, search_file_by_name_or_id

def main(args):
    config = load_config()
    repos_config = load_remote_config()

    search_result = search_file_by_name_or_id(
        args.file_id_or_name,
        repos_config,
        args.repo
    )

    download_files_and_update_repo_status(
        search_result,
        config
    )

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='libs')
    sub_parsers = parser.add_subparsers(help='libs download help')

    parser_cool = sub_parsers.add_parser('download', help='download file from downloaded repos')
    parser_cool.add_argument('file_id_or_name', type=str, help='the file to download')
    parser_cool.add_argument('--repo', '-r', type=str, help='download a certain file from a certain repo (repo name or id)')
    #TODO: add logic for --all
    parser_cool.add_argument('--all', '-a', action='store_true')
    args = parser.parse_args()

    main(args)