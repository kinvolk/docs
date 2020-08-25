getyaml:
	pip install --user pyyaml

.PHONY: docs
docs:
	for i in `find docs/ -name _index.md`; do python3 ./tools/docs-fetcher.py $${i}; done

all: getyaml docs
