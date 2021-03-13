cmake_minimum_required(VERSION 3.5)

project(QtGui LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# QtCreator supports the following variables for Android, which are identical to qmake Android variables.
# Check http://doc.qt.io/qt-5/deployment-android.html for more information.
# They need to be set before the find_package(Qt5 ...) call.

#if(ANDROID)
#    set(ANDROID_PACKAGE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/android")
#    if (ANDROID_ABI STREQUAL "armeabi-v7a")
#        set(ANDROID_EXTRA_LIBS
#            ${CMAKE_CURRENT_SOURCE_DIR}/path/to/libcrypto.so
#            ${CMAKE_CURRENT_SOURCE_DIR}/path/to/libssl.so)
#    endif()
#endif()
include_directories(
  ${Qt5Core_INCLUDE_DIRS}
  ${Qt5Widgets_INCLUDE_DIRS}
  ${tinyxml_INCLUDE_DIRS}
  ${Qt5Qml_INCLUDE_DIRS}
  ${Qt5Quick_INCLUDE_DIRS}
  ${Qt5QuickControls2_INCLUDE_DIRS}
  ${QGuiApplication_INCLUDE_DIRS}
)

set (CMAKE_AUTOMOC ON)

add_definitions(
  ${Qt5Core_DEFINITIONS}
  ${Qt5Widgets_DEFINITIONS}
  ${Qt5Qml_DEFINITIONS}
  ${Qt5Quick_DEFINITIONS}
  ${Qt5QuickControls2_DEFINITIONS}
)

find_package(Qt5 COMPONENTS Core Quick LinguistTools Widgets REQUIRED)
#find_package(QtQuick COMPONENTS QGuiApplication REQUIRED)

set(TS_FILES QtGui_en_150.ts)

if(ANDROID)
    add_library(QtGui SHARED
      main.cpp
      qml.qrc
      ${TS_FILES}
    )
else()
    add_executable(QtGui
      main.cpp
      qml.qrc
      ${TS_FILES}
    )
endif()

target_compile_definitions(QtGui
  PRIVATE $<$<OR:$<CONFIG:Debug>,$<CONFIG:RelWithDebInfo>>:QT_QML_DEBUG>)
target_link_libraries(QtGui PRIVATE Qt5::Core Qt5::Quick Qt5::QuickControls2 Qt5::QGuiApplication)

qt5_create_translation(QM_FILES ${CMAKE_SOURCE_DIR} ${TS_FILES})
