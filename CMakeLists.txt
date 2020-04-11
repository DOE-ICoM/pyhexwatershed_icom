cmake_minimum_required(VERSION 3.10)
project(hexcoastal CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_VERBOSE_MAKEFILE ON)

Include_directories(../hexcoastal/src)

file(GLOB hexcoastal_srcs ../hexcoastal/src/conversion.cpp
        ../hexcoastal/src/conversion.h
        ../hexcoastal/src/data.cpp
        ../hexcoastal/src/data.h
        ../hexcoastal/src/depression.cpp
        ../hexcoastal/src/depression.h
        ../hexcoastal/src/domain.cpp
        ../hexcoastal/src/domain.h
        ../hexcoastal/src/global.cpp
        ../hexcoastal/src/global.h
        ../hexcoastal/src/hexagon.cpp
        ../hexcoastal/src/hexagon.h
        ../hexcoastal/src/main.cpp
        ../hexcoastal/src/segment.cpp
        ../hexcoastal/src/segment.h
        ../hexcoastal/src/system.cpp
        ../hexcoastal/src/system.h
        ../hexcoastal/src/vertex.cpp
        ../hexcoastal/src/vertex.h
        ../hexcoastal/src/watershed.cpp
        ../hexcoastal/src/watershed.h)

add_executable(hexcoastal ${hexcoastal_srcs})

set(default_build_type Debug)
if(EXISTS "${CMAKE_SOURCE_DIR}/../hexcoastal/.git")
    set(default_build_type Release)
endif()

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
      STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
    "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

message("build type = ${default_build_type}")

target_compile_options(hexcoastal PUBLIC -std=c++11)

set(INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../hexcoastal/bin)
install(TARGETS hexcoastal RUNTIME DESTINATION ${INSTALL_DIR})

find_package(OpenMP)

if (OPENMP_FOUND)
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

set(GDAL_INCLUDE_DIR "/share/apps/gdal/2.3.1/include/")
set(GDAL_LIBRARY "/share/apps/gdal/2.3.1/lib/libgdal.so")
include_directories(${GDAL_INCLUDE_DIR})
find_package(GDAL)

set(NETCDF_INCLUDE_DIR "/share/apps/netcdf/4.6.3/gcc/8.1.0/include/")
set(NETCDF_LIBRARY "/share/apps/netcdf/4.6.3/gcc/8.1.0/lib/libnetcdf.so")
include_directories(${NETCDF_INCLUDE_DIR})
find_package(NETCDF)



message("GDAL_LIBRARY = ${GDAL_LIBRARY}")

target_link_libraries(hexcoastal ${GDAL_LIBRARY} -std=c++11)
