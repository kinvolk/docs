all: getdeps docs

getdeps:
	pip3 install --upgrade pyyaml

.PHONY: docs
docs:
	@echo "Fetching external docs…"
	@for i in `find docs/ -name _index.md`; do python3 ./tools/docs-fetcher.py $${i}; echo; done
