cmake_minimum_required (VERSION 3.8)

project ("CNN_Project")

# Activez Rechargement à chaud pour les compilateurs MSVC si cela est pris en charge.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

set(SOURCES
    "src/CNN_Project.cpp"
    "include/CNN_Project.h"
    "python/module_TI.py"
)

find_package(Python REQUIRED)
add_executable(CNN_Project src/CNN_Project.cpp "src/CNN_Project.cpp")
target_include_directories(CNN_Project PRIVATE include)
target_include_directories(CNN_Project PRIVATE C:/Python38/include)
target_link_libraries(CNN_Project PRIVATE C:/Python38/libs/python38.lib)
target_include_directories(CNN_Project PRIVATE C:/Python38/Lib/site-packages)

foreach(SOURCE ${SOURCES})
    configure_file(${SOURCE} ${CMAKE_BINARY_DIR}/${SOURCE} COPYONLY)
endforeach()

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET CNN_Project PROPERTY CXX_STANDARD 20)
endif()