cmake_minimum_required(VERSION 3.5)

project(PRACTICAL_CPP_SOCKETS)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# specify the packages folders

set(PRACTICAL_SOCKET_DIR PracticalSocket)
add_subdirectory(${PRACTICAL_SOCKET_DIR})

set(SUNOSLIBS "")
set(WINLIBS "")
set(WINSOCKLIB "")

if (WIN32)
    set(WINLIBS pthreadVC.lib)
    set(WINSOCKLIB "wsock32 ws2_32")
endif()

if(__SUNOS_COMPILER_GNU)
    set(SUNOSLIBS "socket nsl")
endif()

target_link_libraries(${PROJECT_NAME}
    ${SUNOSLIBS} ${WINLIBS}
)