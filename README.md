# Bazel to CMake integration

[![test](https://github.com/andreiavrammsd/bazel-to-cmake-integration/workflows/test/badge.svg)](https://github.com/andreiavrammsd/bazel-to-cmake-integration/actions/workflows/test.yml)

## What

### Just an experiment

If you need to included, in a CMake project, libraries that are built with Bazel, there are several ways to do it. Many ways end up in requiring you to hardcode all the Bazel paths into your CMakeLists.txt files or to write a packaging tool that finds out all the paths where Bazel generates the files, and then copy them into a location you can use in your CMakeLists.txt files.

This project is a CMake module that attempts to automate almost everything. You set the path to the Bazel project's workspace and then just refer to the Bazel target you need by its name.

This is an experiment. The implementation is coupled to Bazel's internal directory structure and I don't know if it's something stable. And it requires that dependencies that the Bazel projects have to use an "include" directory that will be added to your CMake's target include directories.

- Is this useful? No.

- Was it fun to develop? Yes.

- Is this mature? No.

- Developed and tested only on Ubuntu.

###

Instead of

```cmake
add_executable(my_program main.cpp)

target_include_directories(my_program /path/to/bazel-project
    /hardcoded-path/to/dependency-of-bazel-project/include
    /hardcoded-path/to/dependencya-of-dependency-of-bazel-project/include
    /hardcoded-path/to/dependencyb-of-dependency-of-bazel-project/include
    /hardcoded-path/to/dependencyc-of-dependency-of-bazel-project/include
    ...
)

target_link_directories(my_program /path/to/bazel-project
    /hardcoded-path/to/dependency1-lib
    ...
)

target_link_libraries(my_program dependency1-lib ...)

```

you can have

```cmake
list(APPEND CMAKE_MODULE_PATH /path/to/bazel-to-cmake-integration)
include(bazel)

add_executable(my_program main.cpp)

set(BAZEL_WORKSPACE /hardcoded-path/to/bazel-project)
bazel(hello PRIVATE //:bazel-project)

target_link_libraries(my_program bazel-project)
```

## Why

## How to use

### Requirements

Besides the
CMake and Bazel...
python3.12?
cmake2.8?

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

Tested only on Ubuntu
