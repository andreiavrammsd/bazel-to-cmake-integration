.PHONY: build test clean docker

build:
	mkdir -p build && cd build && cmake ../main_project/cmk && make && ./hello

test:
	python3 test.py

clean:
	rm -rf build
	find -L -name "bazel-*" -exec dirname {} \; | sort -u | while read -r d; do (cd "$$d" && bazel clean --expunge); done

docker:
	docker build -t bazel-to-cmake-integration -f .devcontainer/Dockerfile .
	docker run --rm -ti -v $(shell pwd):/project bazel-to-cmake-integration bash
