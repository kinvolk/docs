import yaml
import sys
import os
import subprocess

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
    repo_name = os.path.basename(repo_url) + branch.replace('/', '_')
    repo_path = os.path.join(TOP_DIR_PATH, EXTERNAL_REPOS_DIR, repo_name)
    if not os.path.isdir(repo_path):
        subprocess.run(['git', 'clone', '--depth=1', '--branch={}'.format(branch), repo_url, repo_path])
    return repo_name

def fetch_docs(file_path):
    yaml_contents = get_yaml(file_path)
    front_matter = yaml.load(yaml_contents, Loader=Loader)

    latest_version = ''
    external_docs = []
    dir_name = os.path.basename(os.path.dirname(file_path))

    for docs in front_matter['external_docs']:
        repo_name = clone_repo(docs['repo'], docs['name'], docs['branch'])
        docs['repo_name'] = repo_name
        docs['file'] = file_path
        if docs.get('is_latest'):
            latest_version = docs['name']
        external_docs.append(docs)

    if not latest_version and external_docs:
        latest_version = external_docs[0]['name']

    create_redirect(dir_name, latest_version)

    return external_docs

def link_external_docs(external_docs):
    for docs in external_docs:
        src_dir = os.path.join('..', '..', EXTERNAL_REPOS_DIR, docs['repo_name'], docs['dir'])
        dst_dir = os.path.join(TOP_DIR_PATH, 'docs', os.path.dirname(docs['file']), docs['name'])
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
    os.makedirs(redirect_dir)

    with open(os.path.join(redirect_dir, 'index.html'), 'w') as f:
        f.write(html_contents)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please pass a file path to it.')
        exit(-1)

    external_docs = fetch_docs(sys.argv[1])
    link_external_docs(external_docs)
