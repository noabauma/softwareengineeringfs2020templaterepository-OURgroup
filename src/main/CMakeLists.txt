cmake_minimum_required(VERSION 3.5)
project(MAIN)

# link_directories(${A_BINARY_DIR}) # this is n2
add_executable(${PROJECT_NAME} main.cc server.cpp jsonxx.cc hospital.cpp parser.cpp)

target_link_libraries(${PROJECT_NAME}
    #PACKAGE_EXAMPLE
    PRACTICAL_CPP_SOCKETS
)
