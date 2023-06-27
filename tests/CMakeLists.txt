cmake_minimum_required(VERSION 3.5)

# view this https://cliutils.gitlab.io/modern-cmake/chapters/testing/googletest.html for more
# information about testing with cmake and gtest
project(Test)

# set project source directory relative to the tests foflder
set(PROJECT_SOURCE_DIR ..)
set(PROJECT_DIR ..)

add_subdirectory("${PROJECT_SOURCE_DIR}/extern/googletest" "extern/googletest")

# add include directories e.g.:
# include_directories(src)


mark_as_advanced(
    BUILD_GMOCK BUILD_GTEST BUILD_SHARED_LIBS
    gmock_build_tests gtest_build_samples gtest_build_tests
    gtest_disable_pthreads gtest_force_shared_crt gtest_hide_internal_symbols
)

# macro to add tests
macro(package_add_test TESTNAME)
    # create an exectuable in which the tests will be stored
    add_executable(${TESTNAME} ${ARGN})
    # link the Google test infrastructure, mocking library, and a default main fuction to
    # the test executable.  Remove g_test_main if writing your own main function.
    target_link_libraries(${TESTNAME} gtest gmock gtest_main)
    # gtest_discover_tests replaces gtest_add_tests,
    # see https://cmake.org/cmake/help/v3.10/module/GoogleTest.html for more options to pass to it
    gtest_discover_tests(${TESTNAME}
        # set a working directory to your project root so that you can find test data via paths relative to the project root
        WORKING_DIRECTORY ${PROJECT_DIR}
        PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY "${PROJECT_DIR}"
    )
    set_target_properties(${TESTNAME} PROPERTIES FOLDER tests)
endmacro()

macro(package_add_test_with_libraries TESTNAME LIBRARIES)
    add_executable(${TESTNAME} ${TESTNAME})
    target_link_libraries(${TESTNAME} gtest gmock gtest_main ${LIBRARIES} ${ARGN})
    gtest_discover_tests(${TESTNAME}
        WORKING_DIRECTORY ${PROJECT_DIR}
        PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY "${PROJECT_DIR}"
    )
    set_target_properties(${TESTNAME} PROPERTIES FOLDER tests)
endmacro()

# add your tests (which do not need additional libraries) to run all the time  
# set(TEST_FILES "")
# list(APPEND TEST_FILES greetings_test.cc)
# list(APPEND TEST_FILES another_test.cc)

set(ALL_LIBRARIES "")
# Here add all your packages as libraries to link to 
list(APPEND ALL_LIBRARIES PACKAGE_EXAMPLE)


set(TEST_FILES "")
# add your test files without their extension(.cc)
list(APPEND TEST_FILES packageExample_test)


foreach(test_file ${TEST_FILES})
package_add_test_with_libraries(${test_file} ${ALL_LIBRARIES})
endforeach(test_file)



# Custom Make command to run_all_tests 
add_custom_target(run_all_tests 
                  COMMAND ${TEST_FILES}
                  COMMAND test
                  DEPENDS ${TEST_FILES}
)
