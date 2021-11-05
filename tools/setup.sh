#!/usr/bin/bash

set -e
set -u
set -o pipefail

CONFIG=${1-""}

if [ -z $CONFIG ]; then
  echo "Please provide a config file"
  exit 1
fi

CONFIG=$(realpath $CONFIG)
ICON="$(python3 ./tools/read-yaml.py $CONFIG params.icon)"
echo $ICON
if [ ! -z $ICON ]; then
  curl -L -o ./site/static/media/logo.svg $ICON
fi

cd site
ln -sf $CONFIG ext_config.yaml
find ./content/docs -maxdepth 1 -type l -delete
python3 ../tools/docs-fetcher.py ./ext_config.yaml
