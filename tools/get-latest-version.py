#!/bin/env python3
#
# This script will read a given markdown file's front-matter (see Hugo's definition for context)
# and output the latest version name for the docs.
#

import os
import subprocess
import sys

import yaml
from yaml import load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

docsfetcher = __import__('docs-fetcher')

def get_latest_version(file_path):
    yaml_contents = docsfetcher.get_yaml(file_path)
    front_matter = yaml.load(yaml_contents, Loader=Loader)

    latest_version = ''

    external_docs = front_matter.get('external_docs', [])

    if not external_docs:
        sys.stderr.write('Warning: No external docs in {}\n'.format(file_path))
        exit(0)

    # i.e. The first version defined in the YAML definition is considered to be the latest.
    if not latest_version:
        latest_version = external_docs[0]['name']

    if latest_version:
        print(latest_version)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please pass a file path to it.')
        exit(-1)

    get_latest_version(sys.argv[1])
