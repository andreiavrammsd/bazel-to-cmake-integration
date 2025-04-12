set(BAZEL_WORKSPACE)
set(BAZEL_ARGS "")
set(BAZEL_DEBUG OFF)
set(BAZEL_DEBUG_MESSAGE_LIMIT 0)
set(BAZEL_BUILD_TARGET ON)
set(BAZEL_PYTHON_PATH python3)
set(BAZEL_EXEC bazel)

set(_THIS_MODULE_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}")

function(bazel cmake_target cmake_visibility bazel_target)
  if(NOT BAZEL_WORKSPACE)
    message(FATAL_ERROR "BAZEL_WORKSPACE is not set")
  endif()
  
  debug("START: ${cmake_target} -> ${bazel_target}")
  debug("WORKSPACE: ${BAZEL_WORKSPACE}")
  debug("BAZEL ARGUMENTS: ${BAZEL_ARGS}")
  debug("BAZEL BUILD TARGET: ${BAZEL_BUILD_TARGET}")

  build_bazel_target(${bazel_target})

  set_include_directories(${bazel_target} INCLUDE_DIRS)
  target_include_directories(${cmake_target} ${cmake_visibility} ${INCLUDE_DIRS})

  set_link_directories(${bazel_target} LINK_DIRS)
  target_link_directories(${cmake_target} ${cmake_visibility} ${LINK_DIRS})

  debug("END: ${cmake_target} -> ${bazel_target}\r\n")
endfunction()

function(debug message)
  if (BAZEL_DEBUG)
    message(STATUS ${message})
  endif()
endfunction()

function(build_bazel_target bazel_target)
  if (BAZEL_BUILD_TARGET)
    set(CMD "${BAZEL_EXEC} build ${BAZEL_ARGS} ${bazel_target}")
    run_command(${CMD} OUT)
  endif()
endfunction()

function(set_include_directories bazel_target INCLUDE_DIRS)
  set(CMD "${BAZEL_EXEC} query deps\(${bazel_target}\) --output xml")
  run_command(${CMD} INCLUDES_XML)

  file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/temp.xml "${INCLUDES_XML}")

  set(CMD "${BAZEL_PYTHON_PATH} ${_THIS_MODULE_BASE_DIR}/bazel.py ${CMAKE_CURRENT_BINARY_DIR}/temp.xml")
  run_command(${CMD} INCLUDES_LIST)

  string(REPLACE "\n" ";" INCLUDES "${INCLUDES_LIST}")
  set(${INCLUDE_DIRS} "${INCLUDES}" PARENT_SCOPE)
endfunction()

function(set_link_directories bazel_target LINK_DIRS)
  set(CMD "${BAZEL_EXEC} cquery ${BAZEL_ARGS} --output=files ${bazel_target}")
  run_command(${CMD} FILES)

  set(DIRECTORIES "")
  foreach(FILE IN LISTS FILES)
      get_filename_component(DIR ${FILE} DIRECTORY)
      list(APPEND DIRECTORIES "${BAZEL_WORKSPACE}/${DIR}")
  endforeach()

  set(${LINK_DIRS} "${DIRECTORIES}" PARENT_SCOPE)
endfunction()

function(run_command cmd OUTPUT)
  debug(${cmd})

  string(REGEX MATCHALL "[^ ]+" CMD_LIST "${cmd}")
  execute_process(
      COMMAND ${CMD_LIST}
      WORKING_DIRECTORY ${BAZEL_WORKSPACE}
      RESULT_VARIABLE CMD_RESULT
      OUTPUT_VARIABLE CMD_OUTPUT
      ERROR_VARIABLE CMD_ERROR
      TIMEOUT 60
  )
  if(CMD_RESULT EQUAL 0)
      set(${OUTPUT} ${CMD_OUTPUT} PARENT_SCOPE)
  else()
      message(FATAL_ERROR "Failed: ${cmd} (exit: ${CMD_RESULT})\r\n${CMD_ERROR}")
  endif()
endfunction()
