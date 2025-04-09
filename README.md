# Bazel to CMake integration

[![test](https://github.com/andreiavrammsd/bazel-to-cmake-integration/workflows/test/badge.svg)](https://github.com/andreiavrammsd/bazel-to-cmake-integration/actions/workflows/test.yml)

## What


## Why


## How to use

### Examples

You need to add the cmake module, set the options you need, add the bazel target, and link the bazel target to the cmake target if necessary.

```cmake
set(PROJECT_ROOT /workspace)
list(APPEND CMAKE_MODULE_PATH ${PROJECT_ROOT}/path/to/bazel-to-cmake-integration)
include(bazel)

add_executable(my_program main.cpp)

set(BAZEL_WORKSPACE ${PROJECT_ROOT}/path/to/bazel-project)
set(BAZEL_DEBUG ON)
set(BAZEL_DEBUG_MESSAGE_LIMIT 1550)
set(BAZEL_ARGS "--config=warnings -c dbg")
set(BAZEL_BUILD_TARGET ON)
set(BAZEL_SHELL /bin/sh)
set(BAZEL_PYTHON_PATH python3)

bazel(hello PRIVATE //:bazel-project)
target_link_libraries(my_program bazel-project)
```

### Options

| Option                      | Description             | Default Value |
|----------------------------|--------------------------|----------------|
| BAZEL_WORKSPACE            | Full path to the bazel project workspace. The only mandatory options.                         | ""             |
| BAZEL_DEBUG                |                          | OFF            |
| BAZEL_DEBUG_MESSAGE_LIMIT  |                          | 0              |
| BAZEL_ARGS                 |                          | ""             |
| BAZEL_BUILD_TARGET         |                          | ON             |
| BAZEL_SHELL                |                          | ""             |
| BAZEL_PYTHON_PATH          |                          | python3        |


## Development status
