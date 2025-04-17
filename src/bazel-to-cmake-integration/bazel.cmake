set(BAZEL_WORKSPACE)
set(BAZEL_ARGS "")
set(BAZEL_DEBUG OFF)
set(BAZEL_DEBUG_MESSAGE_LIMIT 0)
set(BAZEL_BUILD_TARGET ON)
set(BAZEL_PYTHON_PATH python3)
set(BAZEL_EXEC bazel)

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
  debug("${BAZEL_EXEC} query deps\(${bazel_target}\) --output xml")
  debug("${BAZEL_PYTHON_PATH} -c \"${_PYTHON_DEPS_PARSER}\"")

  execute_process(
    COMMAND ${BAZEL_EXEC} query deps\(${bazel_target}\) --output xml
    COMMAND ${BAZEL_PYTHON_PATH} -c "${_PYTHON_DEPS_PARSER}"
    OUTPUT_VARIABLE INCLUDES_LIST
    WORKING_DIRECTORY ${BAZEL_WORKSPACE}
    RESULT_VARIABLE CMD_RESULT
    OUTPUT_VARIABLE CMD_OUTPUT
    ERROR_VARIABLE CMD_ERROR
    TIMEOUT 20
  )
  if(CMD_RESULT EQUAL 0)
    string(REPLACE "\n" ";" INCLUDES "${CMD_OUTPUT}")
    set(${INCLUDE_DIRS} "${INCLUDES}" PARENT_SCOPE)
  else()
      message(FATAL_ERROR "Failed: ${cmd} (exit: ${CMD_RESULT})\r\n${CMD_ERROR}")
  endif()
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
      TIMEOUT 20
  )
  if(CMD_RESULT EQUAL 0)
      set(${OUTPUT} ${CMD_OUTPUT} PARENT_SCOPE)
  else()
      message(FATAL_ERROR "Failed: ${cmd} (exit: ${CMD_RESULT})\r\n${CMD_ERROR}")
  endif()
endfunction()

set(_PYTHON_DEPS_PARSER "
import sys
import pathlib
import xml.etree.ElementTree as ET

root = ET.fromstring(sys.stdin.read())

for node in root.iter('rule'):
    if node.get('class') == 'cc_library':
        base = pathlib.Path(node.get('location')).parent
        print(base.as_posix())
        for i in node.findall('.//list[@name=\"includes\"]/string'):
            print((base / pathlib.Path(i.get('value'))).as_posix())
")
