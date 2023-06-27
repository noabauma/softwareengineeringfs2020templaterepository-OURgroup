cmake_minimum_required(VERSION 3.5)

option(PACKAGE_TESTS "Build the tests" ON)

project(CAS)

# make the build directory where all the binaries will be stored
# before running this makefile
# file(MAKE_DIRECTORY build)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

#add_compile_options(-Wall -g -std=c++11 -pthread)
SET(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} "-std=c++11 -pthread")

# specify the packages folders
set(MAIN_DIR src/main)
set(PACKAGE_EXAMPLE_DIR src/packageExample)
# set(YourPackageName_DIR src/YourPackageName)

# set(FUNCTIONS_DIR src/functions)
set(DOCS_DIR doc/doxygen)

include_directories(src)

set(PRACTICAL_SOCKET_DIR src/PracticalSocket)

add_subdirectory(${PRACTICAL_SOCKET_DIR})


# include_directories(${MAIN_DIR}) # You can also use that if you want to directly include files from inside the package
add_subdirectory(${MAIN_DIR})
add_subdirectory(${PACKAGE_EXAMPLE_DIR})
# add_subdirectory(${YourPackageName_DIR}) # Add more as you add packages


if (CMAKE_BUILD_TYPE MATCHES "^[Rr]elease")
    add_subdirectory(${DOCS_DIR})
endif()


# add_executable(CAS src/main/main.cc) # On releases this line could be uncommented


if(PACKAGE_TESTS)
    enable_testing()
    include(GoogleTest)
    add_subdirectory(tests)
endif()
