# Bazel to CMake integration

[![test](https://github.com/andreiavrammsd/bazel-to-cmake-integration/actions/workflows/test.yml/badge.svg)](https://github.com/andreiavrammsd/bazel-to-cmake-integration/actions/workflows/test.yml)

## What is this?

### Intro

You have a CMake project. And you need to include some libraries that are built with Bazel. You can build the libraries, then copy the headers and the object files to some locations that you will use in CMake. Or package the libraries somehow. Unless they are an active part of the CMake project and you need to work on them actively and see the changes live.

`Bazel to CMake integration` is a CMake module that allows easier integration of Bazel targets into CMake projects.

This project came from a real need but it is not properly tested. It's probably not useful and not portable, but it was fun developing it. __It's just an experiment.__

### Basic usage

Instead of

```cmake
add_executable(my_program main.cpp)

target_include_directories(my_program /path/to/bazel-project
    /path/to/dependency-of-bazel-project/include
    /path/to/dependencya-of-dependency-of-bazel-project/include
    /path/to/dependencyb-of-dependency-of-bazel-project/include
    /path/to/dependencyc-of-dependency-of-bazel-project/include
    ...
)

target_link_directories(my_program /path/to/bazel-project
    /path/to/dependency1-lib
    ...
)

target_link_libraries(my_program dependency1-lib ...)

```

you can have

```cmake
list(APPEND CMAKE_MODULE_PATH /path/to/bazel-to-cmake-integration)
include(bazel)

add_executable(my_program main.cpp)

set(BAZEL_WORKSPACE /path/to/bazel-project)
bazel(hello PRIVATE //:bazel-project)

target_link_libraries(my_program bazel-project)
```

## Installation and requirements

Copy the [bazel.cmake](https://raw.githubusercontent.com/andreiavrammsd/bazel-to-cmake-integration/refs/heads/master/src/bazel-to-cmake-integration/bazel.cmake) file into your project. You need the following:

| Tool             | Version                           |
|------------------|-----------------------------------|
| CMake            | 3+                              |
| Python           | 3.5+                              |
| Bazel            | 7+                 |
| Linux            | Tested only on Ubuntu 24.04|

You can automate installation:

```cmake
set(BAZEL_TO_CMAKE_INTEGRATION_LOCATION "/tmp/bazel-to-cmake-integration")
if(NOT (EXISTS ${BAZEL_TO_CMAKE_INTEGRATION_LOCATION}))
  message(STATUS "Downloading bazel-to-cmake-integration ${BAZEL_TO_CMAKE_INTEGRATION_LOCATION}")
  file(DOWNLOAD https://raw.githubusercontent.com/andreiavrammsd/bazel-to-cmake-integration/refs/heads/master/src/bazel-to-cmake-integration/bazel.cmake ${BAZEL_TO_CMAKE_INTEGRATION_LOCATION}/bazel.cmake)
endif()
```

## Usage

You need to add the CMake module to your project, set the path to Bazel workspace and other options you may need, connect the Bazel target to the CMake one, and link the Bazel library to the CMake target if necessary.

The module accepts some [options](#options) and has a `bazel` function that accepts three arguments: CMake target, visibility, Bazel target.

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

The options are set globally. Set them before any Bazel target that needs other options.

See the [test project](./src/test/project/main_project/cmk/CMakeLists.txt).

### Options

| Option                      | Description             | Default value |
|----------------------------|--------------------------|----------------|
| BAZEL_WORKSPACE            | Full path to the Bazel project workspace. The only mandatory option.                         | \<none\>             |
| BAZEL_DEBUG                | Print debug messages during the CMake build.                         | OFF            |
| BAZEL_DEBUG_MESSAGE_LIMIT  | Limit of a debug message length. 0 means no limit.                         | 0              |
| BAZEL_ARGS                 | A string with Bazel arguments (eg: --config=warnings -c opt).                         | ""             |
| BAZEL_BUILD_TARGET         | Whether to build the Bazel target during the CMake build. Set it to OFF if you want build it before anything.                         | ON             |
| BAZEL_SHELL                | Shell to use.                         | /bin/bash             |
| BAZEL_PYTHON_PATH          | Python executable.                         | python3        |
