cmake_minimum_required(VERSION 3.5)

project(PACKAGE_EXAMPLE)

# set(PROJECT_SOURCE_DIR ../..)
# set(PROJECT_DIR ..)

include_directories(..)
# add_subdirectory("${PROJECT_SOURCE_DIR}/extern/googletest" "extern/googletest")
# set the source files of this directory
set(${PROJECT_NAME}_SRCS "")
# Here append to the sources list your .cc/.cpp files
list(APPEND ${PROJECT_NAME}_SRCS dummyClass.cc)
#list(APPEND ${PROJECT_NAME}_SRCS yourClass.cc)

add_library(${PROJECT_NAME} ${PACKAGE_EXAMPLE_SRCS})


# link to other packages
target_link_libraries(${PROJECT_NAME}
    #name of package to link e.g. PACKAGE_EXAMPLE_2 or MAIN
)

# include the ./src directory
target_include_directories( ${PROJECT_NAME}
    PUBLIC ${PROJECT_SOURCE_DIR}
)
