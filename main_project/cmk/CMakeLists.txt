cmake_minimum_required(VERSION 3.10)
project(HelloWorld)


list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")
include(bazel)

add_executable(hello main.cpp)

cmake_path(GET PROJECT_SOURCE_DIR PARENT_PATH PARENT_DIR)
cmake_path(GET PARENT_DIR PARENT_PATH PARENT_DIR)

set(BAZEL_WORKSPACE ${PARENT_DIR}/main_project)
set(BAZEL_DEBUG ON)
bazel(hello PRIVATE //bzl:bzl)
target_link_libraries(hello bzl)

set(BAZEL_PYTHON_PATH python3)
set(BAZEL_WORKSPACE ${PARENT_DIR}/bzl_world)
set(BAZEL_DEBUG ON)
set(BAZEL_DEBUG_MESSAGE_LIMIT 1550)
set(BAZEL_ARGS "--config=warnings -c dbg")
bazel(hello PRIVATE //:world)
target_link_libraries(hello world)

set(BAZEL_WORKSPACE ${PARENT_DIR}/bzl_header_only)
set(BAZEL_DEBUG OFF)
set(BAZEL_ARGS "-c opt")
set(BAZEL_SHELL /bin/sh)
set(BAZEL_BUILD_TARGET OFF)
bazel(hello PUBLIC //:header)
