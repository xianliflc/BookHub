from src.libs.objects.config_object import ConfigObject
from src.libs.download import load_remote_config_file
from src.templates.templates import remote_repo_template
from jsonschema import Draft7Validator, draft7_format_checker, exceptions, validate

import json, os

from src.vendors.vendors import SUPPORTED_VENDORS
DEFAULT_RESOURCE_VENDOR = 'Github'
REMOTE_REPO_SCHEMA = '..\\..\\schemas\\remote_repo_schema.json'

class RemoteRepoException(Exception):
    pass

def download_remote_config(
    url: str
):
    config_data = load_remote_config_file(url)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, REMOTE_REPO_SCHEMA)
    with open(filename, 'r') as schema_file:
        schema = json.load(schema_file)
        config_json = json.loads(config_data)
        try:
            Draft7Validator.check_schema(schema)
            validate(instance=config_json, schema=schema, format_checker = draft7_format_checker)
            return config_json
        except exceptions.ValidationError as e:
            raise RemoteRepoException('Invalid remote repo config file: ' + e)

def create_remote_repo_config(
    data: dict
) -> dict:
    data['version'] = 1

    the_template = remote_repo_template.copy()
    the_template.update(data)

    error_message = ''
    has_error = False
    if not the_template['name']:
        has_error = True
        error_message += ' missing name'
    if not the_template['resource_vendor'] or \
        (the_template['resource_vendor'] and the_template['resource_vendor'] not in SUPPORTED_VENDORS):
        the_template['resource_vendor'] = DEFAULT_RESOURCE_VENDOR
    if not the_template['url']:
        has_error = True
        error_message += ' missing url' 
    if not the_template['maintainer']:
        has_error = True
        error_message += ' missing maintainer'  

    if has_error:
        raise RemoteRepoException('ERROR: manipulating remote repo config:' + error_message)
    return the_template

def output_remote_repo_config(
    data: dict,
    config: ConfigObject,
    filename: str
):
    output_path = config.system['remote_repo_config_output_path']
    json_object = json.dumps(data, indent = 4)
    if not os.path.exists(output_path):
        access = 0o777
        os.makedirs(output_path, access)    
    file_path = os.path.join(output_path, filename +'.bh')
    with open(file_path, "w") as outfile:
        outfile.write(json_object)
        return file_path

def create_and_output_remote_repo_config(
    data: dict,
    config: ConfigObject,
    filename: str
) -> None:
    remote_repo_config = create_remote_repo_config(data)
    output_remote_repo_config(remote_repo_config, config, filename)