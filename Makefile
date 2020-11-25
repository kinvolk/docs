all: getdeps docs

getdeps:
	pip3 install --upgrade pyyaml

.PHONY: docs
docs:
	@echo "Fetching external docs…"
	# Remove existing links first
	@find ./docs -maxdepth 2 -type l -delete
	@python3 ./tools/fcl-fetch-version-data.py ./docs/flatcar-container-linux/_index.md.in > ./docs/flatcar-container-linux/_index.md
	@for i in `find docs/ -name _index.md`; do python3 ./tools/docs-fetcher.py $${i}; echo; done
