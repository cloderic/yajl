#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import subprocess
import shutil

defaultSourceDirectory = os.path.abspath("../..")
defaultBuildDirectory = os.path.abspath("./xcode/")
defaultInstallDirectory = os.path.abspath("../../install/ios")
defaultToolchain = os.path.abspath("iOS.cmake")
 
def main():
    parser = argparse.ArgumentParser(description="Building YAJL for iOS")
    parser.add_argument("-c", "--clean", help="Clean cmake generated file before the new generation", action="store_true")
    parser.add_argument("-s", "--simulator", help="Build for the simulator", action="store_true")
    parser.add_argument("--source_directory", help="Source directory (default is {})".format(defaultSourceDirectory), default=defaultSourceDirectory)
    parser.add_argument("--build_directory", help="Build directory (default is {})".format(defaultBuildDirectory), default=defaultBuildDirectory)
    parser.add_argument("--install_directory", help="Install directory (default is {})".format(defaultInstallDirectory), default=defaultInstallDirectory)
    parser.add_argument("--toolchain", help="CMake toolchain (default is {})".format(defaultToolchain), default=defaultToolchain)
    args = parser.parse_args()

    # clean the build directory if asked
    if args.clean and os.path.exists(args.build_directory):
        shutil.rmtree(args.build_directory)

    cwd = os.getcwd()
    
    if not os.path.exists(args.build_directory):
    	os.mkdir(args.build_directory)
    os.chdir(args.build_directory)

    # cmake
    ios_platform = "OS"
    if args.simulator:
        ios_platform = "SIMULATOR"

    cmakeReturnStatus = subprocess.call([
    	"cmake", 
    	"-DCMAKE_TOOLCHAIN_FILE={}".format(args.toolchain),
    	"-DIOS_PLATFORM={}".format(ios_platform),
        "-DBUILD_DYNAMIC_LIBRARY=OFF",
        "-DBUILD_APPLICATIONS=OFF",
        "-DCMAKE_INSTALL_PREFIX={}".format(args.install_directory),
    	"-GXcode",
    	"{}".format(args.source_directory)])
    if cmakeReturnStatus != 0:
        print "Error during the cmake call."

    # install debug
    debugInstallReturnStatus = subprocess.call([
        "xcodebuild", 
        "-target", "install",
        "-configuration", "Debug"]);
    if cmakeReturnStatus != 0:
        print "Error during the build and installation of the debug version."

    os.chdir(cwd)
 
if __name__ == "__main__" :
    main()