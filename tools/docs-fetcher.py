#!/bin/env python3
#
# This script will read a given markdown file's front-matter (see Hugo's definition for context)
# and fetch the external docs repos defined in there.
#

import os
import yaml
import subprocess
import sys

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

TOP_DIR_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

YAML_FRONT_MATTER_DELIM = '---'
EXTERNAL_REPOS_DIR = 'external-docs'

def get_yaml(file_path):
    contents = []
    with open(file_path, 'r') as f:
        contents = f.readlines()

    yaml_contents = ''
    for i in range(len(contents)):
        if contents[i].startswith(YAML_FRONT_MATTER_DELIM):
            for j in range(1 + 1, len(contents)):
                if contents[j].startswith(YAML_FRONT_MATTER_DELIM):
                    break
                yaml_contents += contents[j]
            break

    return yaml_contents

def clone_repo(repo_url, name, branch):
    repo_name = os.path.basename(repo_url) + '_' + branch.replace('/', '_')
    repo_path = os.path.join(TOP_DIR_PATH, EXTERNAL_REPOS_DIR, repo_name)
    if not os.path.isdir(repo_path):
        subprocess.run(['git', 'clone', '--depth=1', '--branch={}'.format(branch), repo_url, repo_path])
    return repo_name

def fetch_docs(file_path):
    yaml_contents = get_yaml(file_path)
    front_matter = yaml.load(yaml_contents, Loader=Loader)

    latest_version = ''
    dir_name = os.path.basename(os.path.dirname(file_path))

    external_docs = front_matter.get('external_docs', [])

    if not external_docs:
        print('Warning: No external docs in', file_path)
        exit(0)

    for docs in external_docs:
        repo_name = clone_repo(docs['repo'], docs['name'], docs['branch'])
        docs['repo_name'] = repo_name
        docs['file'] = file_path
        if docs.get('is_latest'):
            latest_version = docs['name']

        link_external_docs(os.path.join(repo_name, docs['dir']), os.path.join(dir_name, docs['name']))

    # If the docs didn't define the latest version, then we assume is the first one defined,
    # i.e. at the top in the YAML definition.
    if not latest_version:
        latest_version = external_docs[0]['name']

    # We should create a link "latest" pointing to the latest docs' version
    create_redirect(dir_name, latest_version)

def link_external_docs(linked_dir, link_name):
    src_dir = os.path.join('..', '..', EXTERNAL_REPOS_DIR, linked_dir)
    dst_dir = os.path.join(TOP_DIR_PATH, 'docs', link_name)

    if os.path.exists(dst_dir):
        if os.path.islink(dst_dir) and os.readlink(dst_dir) == src_dir:
            # All is good, we already have the desired link
            return

        print('File exists when trying to create link', dst_dir)
        return

    os.symlink(src_dir, dst_dir)

def create_redirect(folder, target, redirect_name='latest'):
    html_contents = '''<!DOCTYPE html>
<html>
  <head>
    <title></title>
    <link rel="canonical" href="/docs/@DOCS_PATH@"/>
    <meta name="robots" content="noindex">
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <meta http-equiv="refresh" content="0; url=/docs/@DOCS_PATH@"/>
  </head>
</html>
'''
    html_contents = html_contents.replace('@DOCS_PATH@', os.path.join(folder, target))
    redirect_dir = os.path.join(TOP_DIR_PATH, 'docs', folder, redirect_name)

    if os.path.exists(redirect_dir):
        return

    os.makedirs(redirect_dir)

    with open(os.path.join(redirect_dir, 'index.html'), 'w') as f:
        f.write(html_contents)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please pass a file path to it.')
        exit(-1)

    fetch_docs(sys.argv[1])