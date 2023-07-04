#
# Print a message only if the `VERBOSE_OUTPUT` option is on
#

function(verbose_message content)
    if(${PROJECT_NAME}_VERBOSE_OUTPUT)
        message(VERBOSE ${MESSAGE_TYPE} ${content})
    endif()
endfunction()

#
# Add a target for formatting the project using `clang-format` (i.e: cmake --build build --target clang-format)
#

function(add_clang_format_target)
    if(NOT ${PROJECT_NAME}_CLANG_FORMAT_BINARY)
			find_program(${PROJECT_NAME}_CLANG_FORMAT_BINARY clang-format)
    endif()
    if(${PROJECT_NAME}_CLANG_FORMAT_BINARY)
      			if(${PROJECT_NAME}_BUILD_EXECUTABLE)
				add_custom_target(clang-format
						COMMAND ${${PROJECT_NAME}_CLANG_FORMAT_BINARY}
						-i $${CMAKE_CURRENT_LIST_DIR}/${exe_sources} ${CMAKE_CURRENT_LIST_DIR}/${headers})
			elseif(${PROJECT_NAME}_BUILD_HEADERS_ONLY)
				add_custom_target(clang-format
						COMMAND ${${PROJECT_NAME}_CLANG_FORMAT_BINARY}
						-i ${CMAKE_CURRENT_LIST_DIR}/${headers})
			else()
				add_custom_target(clang-format
						COMMAND ${${PROJECT_NAME}_CLANG_FORMAT_BINARY}
						-i ${CMAKE_CURRENT_LIST_DIR}/${sources} ${CMAKE_CURRENT_LIST_DIR}/${headers})
			endif()

			message(STATUS "Format the project using the `clang-format` target (i.e: cmake --build build --target clang-format).\n")
    endif()
endfunction()
