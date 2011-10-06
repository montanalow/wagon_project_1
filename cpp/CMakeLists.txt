cmake_minimum_required(VERSION 2.8)
project(Wagonz)

if(WIN32)
    set(CMAKE_MODULE_PATH "$ENV{OGRE_HOME}/CMake/;${CMAKE_MODULE_PATH}")
    set(OGRE_SAMPLES_INCLUDEPATH "$ENV{OGRE_HOME}/Samples/include")
endif(WIN32)

if(UNIX)
    set(CMAKE_MODULE_PATH "/usr/lib/OGRE/cmake/;${CMAKE_MODULE_PATH}")
    set(OGRE_SAMPLES_INCLUDEPATH "/usr/local/share/OGRE/samples/Common/include")
endif(UNIX)

set(CMAKE_DEBUG_POSTFIX "_d")
set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_BINARY_DIR}/dist")

find_package(OGRE REQUIRED)
if(NOT "${OGRE_VERSION_NAME}" STREQUAL "Cthugha")
    message(SEND_ERROR "You need Ogre 1.7 'Cthugha' to build this app!")
endif()

find_package(OIS REQUIRED)
if(NOT OIS_FOUND)
    message(SEND_ERROR "failed to find OIS!")
endif()

set(HDRS
    ./inc/GameManager.h
)

set(SRCS
    ./src/GameManager.cpp
    ./src/main.cpp
)

include_directories(${OIS_INCLUDE_DIRS}
    ${OGRE_INCLUDE_DIRS}
    ${OGRE_SAMPLES_INCLUDEPATH}
    ./inc
)

add_executable(Wagonz WIN32 ${HDRS} ${SRCS})
set_target_properties(Wagonz PROPERTIES DEBUG_POSTFIX _d)
target_link_libraries(Wagonz ${OGRE_LIBRARIES} ${OIS_LIBRARIES})

file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/dist/bin)
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/dist/media)

#find_program(WSDL2H_CMD wsdl2h)
#if(NOT WSDL2H_CMD)
#    message(FATAL_ERROR "unable to find 'wsdl2h' from the gSOAP package!")
#endif(NOT WSDL2H_CMD)
#
#find_program(SOAPCPP2_CMD soapcpp2)
#if(NOT SOAPCPP2_CMD)
#    message(FATAL_ERROR "unable to find 'soapcpp2' from the gSOAP package!")
#endif(NOT SOAPCPP2_CMD)
#
#set(WSDL_DIR ${CMAKE_SOURCE_DIR}/wsdl)
#set(GENERATED_DIR ${CMAKE_SOURCE_DIR}/src/generated)
#set(GSOAP_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/src/thirdparty/gsoap)
#set(TYPEMAP ${GSOAP_INCLUDE_DIR}/typemap.dat)
#
## C++ source files
#set(SOURCES ${CMAKE_SOURCE_DIR}/src/main.cpp ${GSOAP_INCLUDE_DIR}/stdsoap2.cpp)
#
#file(GLOB WSDL_FILES ${WSDL_DIR}/*.wsdl)
#foreach(FILENAME ${WSDL_FILES})
#    message(STATUS "processing ${FILENAME}")
#    get_filename_component(BASE ${FILENAME} NAME_WE)
#    set(WSDL_OUTPUT ${GENERATED_DIR}/${BASE}.wsdl.h)
#    add_custom_command(
#        OUTPUT ${WSDL_OUTPUT}
#        COMMAND ${WSDL2H_CMD}
#        ARGS # run `wsdl2h -h` to see complete options list
#            -t ${TYPEMAP} # use type map file instead of the default file typemap.dat
#            -o ${WSDL_OUTPUT}
#            ${FILENAME}
#        COMMENT "converting ${BASE} to c++ stub"
#    )
#    set(GENERATED_CPP ${GENERATED_DIR}/soap${BASE}Soap11BindingProxy.cpp)
#    set(GENERATED_MAP ${GENERATED_DIR}/${BASE}Soap11Binding.nsmap)
#    add_custom_command(
#        OUTPUT ${GENERATED_CPP} ${GENERATED_MAP} ${GENERATED_DIR}/soapC.cpp
#        DEPENDS ${WSDL_OUTPUT}
#        COMMAND ${SOAPCPP2_CMD}
#        ARGS
#            -1 # generate SOAP 1.1 bindings
#            -C # generate client-side code only
#            #-S	generate server-side code only
#            #-T	generate server auto-test code
#            -L # don't generate soapClientLib/soapServerLib
#            #-a	use SOAPAction HTTP/WSA header to invoke server-side operations
#            -b # serialize byte arrays char[N] as string
#            #-c      generate C source code
#            -d ${GENERATED_DIR}# use path to save files
#            -e # generate SOAP RPC encoding style bindings
#            #-h	display help info
#            -i # generate service proxies and objects inherited from soap struct
#            -I ${GSOAP_INCLUDE_DIR} # path  use path(s) for #import
#            #-l      generate linkable modules (experimental)
#            #-m      generate Matlab(tm) code for MEX compiler
#            #-n      use service name to rename service functions and namespace table
#            #-pname  save files with new prefix name instead of 'soap'
#            #-qname  use name as the C++ namespace of all declarations
#            #-s      generate deserialization code with strict XML validation checks
#            #-t      generate code for fully xsi:type typed SOAP/XML messaging
#            #-v	display version info
#            -w #	don't generate WSDL and schema files
#            #-x # don't generate sample XML message files
#            ${WSDL_OUTPUT}
#        COMMENT "converting c++ stubs to actual service interface for ${BASE}"
#    )
#    set(SOURCES ${SOURCES} ${GENERATED_CPP} ${GENERATED_DIR}/soapC.cpp)
#    set_source_files_properties(${WSDL_OUTPUT} PROPERTIES GENERATED TRUE)
#    set_source_files_properties(${GENERATED_CPP} PROPERTIES GENERATED TRUE)
#endforeach(FILENAME)
#
#
#add_executable(QuartetAgent ${SOURCES})
#
#
#
##Usage: soapcpp2 [-1|-2] [-C|-S] [-T] [-L] [-a] [-b] [-c] [-d path] [-e] [-h] [-i] [-I path:path:...] [-l] [-m] [-n] [-p name] [-s] [-t] [-v] [-w] [-x] [infile]
##
##-1      generate SOAP 1.1 bindings
##-2      generate SOAP 1.2 bindings
##-C	generate client-side code only
##-S	generate server-side code only
##-T	generate server auto-test code
##-L	don't generate soapClientLib/soapServerLib
##-a	use SOAPAction HTTP/WSA header to invoke server-side operations
##-b	serialize byte arrays char[N] as string
##-c      generate C source code
##-dpath  use path to save files
##-e	generate SOAP RPC encoding style bindings
##-h	display help info
##-i      generate service proxies and objects inherited from soap struct
##-Ipath  use path(s) for #import
##-l      generate linkable modules (experimental)
##-m      generate Matlab(tm) code for MEX compiler
##-n      use service name to rename service functions and namespace table
##-pname  save files with new prefix name instead of 'soap'
##-qname  use name as the C++ namespace of all declarations
##-s      generate deserialization code with strict XML validation checks
##-t      generate code for fully xsi:type typed SOAP/XML messaging
##-v	display version info
##-w	don't generate WSDL and schema files
##-x	don't generate sample XML message files
##infile	header file to parse (or stdin)
##
