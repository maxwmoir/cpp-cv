cmake_minimum_required(VERSION 3.10)

project(opencv LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(opencv main.cpp)

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
target_link_libraries( opencv ${OpenCV_LIBS} )
