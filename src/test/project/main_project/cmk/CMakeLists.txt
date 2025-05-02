cmake_minimum_required(VERSION 3.10)
project(HelloWorld)

set(PROJECT_ROOT /workspace)
list(APPEND CMAKE_MODULE_PATH ${PROJECT_ROOT}/src/bazel-to-cmake-integration)
include(bazel)

add_executable(hello main.cpp)

if (BAZEL_VERSION)
    set(BAZEL_EXEC bazel-${BAZEL_VERSION})
endif()

set(BAZEL_WORKSPACE ${PROJECT_ROOT}/src/test/project/main_project)
set(BAZEL_DEBUG ON)
bazel(hello PRIVATE //bzl:bzl)
target_link_libraries(hello bzl)

set(BAZEL_WORKSPACE ${PROJECT_ROOT}/src/test/project/bzl_world)
set(BAZEL_DEBUG ON)
set(BAZEL_DEBUG_MESSAGE_LIMIT 1550)
set(BAZEL_ARGS "--config=warnings -c dbg")
set(BAZEL_PYTHON_PATH python3)
bazel(hello PRIVATE //:world)
target_link_libraries(hello world)

set(BAZEL_WORKSPACE ${PROJECT_ROOT}/src/test/project/bzl_header_only)
set(BAZEL_DEBUG OFF)
set(BAZEL_ARGS "-c opt")
set(BAZEL_SHELL /bin/sh)
set(BAZEL_BUILD_TARGET OFF)
bazel(hello PUBLIC //:header)
