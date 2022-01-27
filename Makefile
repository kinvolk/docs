all: getdeps
	@echo "Run: ./tools/setup.sh ../PATH/TO/MYPROJECT/CONFIG.YAML"
	@echo "and then: make run"

getdeps:
	pip3 install --upgrade pyyaml

run:
	@cd site && \
	hugo server --buildFuture --watch --disableFastRender --config ./config.yaml\,./ext_config.yaml\,./tmp_modules.yaml

build:
	@cd site && \
	hugo --config ./config.yaml\,./ext_config.yaml -b ${HUGO_BASE_URL}
