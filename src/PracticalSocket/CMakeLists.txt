cmake_minimum_required(VERSION 3.5)

project(PRACTICAL_CPP_SOCKETS)

# set the source files of this directory
set(${PROJECT_NAME}_SRCS "")
list(APPEND ${PROJECT_NAME}_SRCS PracticalSocket.cpp)

add_library(${PROJECT_NAME} ${PRACTICAL_CPP_SOCKETS_SRCS})


set(SUNOSLIBS "")
set(WINLIBS "")
set(WINSOCKLIB "")

if(WIN32)
    set(WINLIBS ${PROJECT_SOURCE_DIR}/pthreadVC.lib)
    set(WINSOCKLIB "wsock32 ws2_32")
endif()

if(__SUNOS_COMPILER_GNU)
    set(SUNOSLIBS "socket nsl")
endif()

target_link_libraries(${PROJECT_NAME}
    ${SUNOSLIBS} ${WINLIBS} ${WINSOCKLIB}
)

target_include_directories( ${PROJECT_NAME}
    PUBLIC ${PROJECT_SOURCE_DIR}
)