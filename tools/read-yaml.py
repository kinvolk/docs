#!/bin/env python3
#
# This script will read a YAML file into a Python dict, and use the given
# argument to return the respective data if it exists, or return nothing
# otherwise.
#

import sys

docsfetcher = __import__('docs-fetcher')

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Please provide a YAML file as the first argument, and a data spec like 'mytopentry.myfield'.",  file=sys.stderr)
    exit(1)

  spec = sys.argv[2]
  yml = docsfetcher.read_yaml(sys.argv[1])

  for word in spec.split('.'):
    if not yml or not isinstance(yml, dict):
      print("Failed to find the requested data from spec.", file=sys.stderr)
      exit(1)

    yml = yml.get(word, None)

  print(yml)
