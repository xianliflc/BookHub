import argparse
from src.libs.config_loader import (
    load_remote_config,
)
from src.services.remote.download_service import search_file_by_name_or_id

def main(args):
    repos_config = load_remote_config()

    search_result = search_file_by_name_or_id(
        args.file_name_or_id,
        repos_config,
        args.repo
    )
    print(search_result)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='libs')
    sub_parsers = parser.add_subparsers(help='libs search help')

    parser_cool = sub_parsers.add_parser('search', help='search file from downloaded repo')
    parser_cool.add_argument('file_name_or_id', type=str, help='the file name to search')
    parser_cool.add_argument('--repo', '-r', type=str, help='search file in a certain repo')

    args = parser.parse_args()

    main(args)