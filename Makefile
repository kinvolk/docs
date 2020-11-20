all: getdeps docs

getdeps:
	pip3 install --upgrade pyyaml

.PHONY: docs
docs:
	@echo "Fetching external docs…"
	@python3 ./tools/fcl-fetch-version-data.py ./docs/flatcar-container-linux/_index.md.in > ./docs/flatcar-container-linux/_index.md
	@for i in `find docs/ -name _index.md`; do python3 ./tools/docs-fetcher.py $${i}; echo; done
