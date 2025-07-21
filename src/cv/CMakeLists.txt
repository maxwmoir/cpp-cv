cmake_minimum_required(VERSION 3.14)
project(opencv LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
FetchContent_MakeAvailable(googletest)

enable_testing()

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )


add_executable(opencv
  main.cpp
  utils.cpp
  utils.h
)
target_link_libraries( opencv ${OpenCV_LIBS} )


add_executable(main_test
  main_test.cc
  utils.cpp
  utils.h
)
target_link_libraries(main_test gtest_main)


include(GoogleTest)
gtest_discover_tests(main_test)
