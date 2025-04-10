set(_THIS_MODULE_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}")

set(BAZEL_WORKSPACE)
set(BAZEL_DEBUG OFF)
set(BAZEL_DEBUG_MESSAGE_LIMIT 0)
set(BAZEL_ARGS "")
set(BAZEL_BUILD_TARGET ON)
set(BAZEL_SHELL "")
set(BAZEL_PYTHON_PATH python3)

function(bazel cmake_target cmake_visibility bazel_target)
  if(NOT BAZEL_WORKSPACE)
    message(FATAL_ERROR "BAZEL_WORKSPACE is not set")
  endif()

  if(BAZEL_DEBUG)
    set(_BAZEL_DEBUG --debug)
  endif()

  set(_BAZEL_DEBUG_MESSAGE_LIMIT --debug-message-limit ${BAZEL_DEBUG_MESSAGE_LIMIT})

  if(NOT BAZEL_ARGS STREQUAL "")
    set(_BAZEL_ARGS --args=${BAZEL_ARGS})
  endif()
  
  if(NOT BAZEL_BUILD_TARGET)
    set(_BAZEL_NO_BUILD --no-build)
  endif()
  
  if(NOT BAZEL_SHELL STREQUAL "")
    set(_BAZEL_SHELL --shell=${BAZEL_SHELL})
  endif()

  execute_process(
    COMMAND ${BAZEL_PYTHON_PATH} ${_THIS_MODULE_BASE_DIR}/bazel.py ${bazel_target} ${_BAZEL_DEBUG} ${_BAZEL_DEBUG_MESSAGE_LIMIT} ${_BAZEL_ARGS} ${_BAZEL_SHELL} ${_BAZEL_NO_BUILD}
    WORKING_DIRECTORY ${BAZEL_WORKSPACE}
    RESULT_VARIABLE RESULT
    OUTPUT_VARIABLE DEPENDENCIES
  )
  if (NOT RESULT EQUAL 0)
    message(FATAL_ERROR "Bazel failed: ${DEPENDENCIES}")
  endif()

  separate_arguments(DIRECTORIES NATIVE_COMMAND ${DEPENDENCIES})
  target_include_directories(${cmake_target} ${cmake_visibility} ${DIRECTORIES})
  target_link_directories(${cmake_target} ${cmake_visibility} ${DIRECTORIES})
endfunction()
