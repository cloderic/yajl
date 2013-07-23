#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import subprocess
import shutil

defaultSourceDirectory = os.path.abspath("..")
defaultBuildDirectory = os.path.abspath("./ios/")
defaultInstallDirectory = os.path.abspath("../install/ios")

def configure_build_and_install(sources_directory, install_directory, simulator):
    xcode_sdk = "iphoneos"
    simulator_cmake = "OFF"
    if simulator:
        xcode_sdk = "iphonesimulator"
        simulator_cmake = "ON"

    returnStatus = subprocess.call([
        "cmake", 
        "-DIOS=ON",
        "-DIOS_SIMULATOR={}".format(simulator_cmake),
        "-DCMAKE_INSTALL_PREFIX={}".format(install_directory),
        "-GXcode",
        "{}".format(sources_directory)])
    
    if returnStatus != 0:
        return False

    return do_build_and_install("Debug",xcode_sdk) and do_build_and_install("Release",xcode_sdk)

def do_build_and_install(configuration, xcode_sdk):
    returnStatus = subprocess.call([
        "xcodebuild", 
        "-target", "install",
        "-configuration", "{}".format(configuration),
        "-sdk","{}".format(xcode_sdk)]);
    if returnStatus != 0:
        return False

    # The following call tricks cmake to workaround a known bug http://www.cmake.org/Bug/view.php?id=12506
    returnStatus = subprocess.call([
        "cmake", 
        "-DBUILD_TYPE={}".format(configuration),
        "-P", "cmake_install.cmake"]);
    if returnStatus != 0:
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Building and installing a cmake project for iOS")
    parser.add_argument("platform", choices=['all', 'simulator', 'device'], nargs='?', help="Target platform (default is %(default)s)", default='all')
    parser.add_argument("--source_directory", help="Source directory (default is %(default)s)", default=defaultSourceDirectory)
    parser.add_argument("--build_directory", help="Build directory (default is %(default)s)", default=defaultBuildDirectory)
    parser.add_argument("--install_directory", help="Install directory (default is %(default)s)", default=defaultInstallDirectory)
    args = parser.parse_args()

    cwd = os.getcwd()
    
    if not os.path.exists(args.build_directory):
    	os.mkdir(args.build_directory)
    os.chdir(args.build_directory)

    if (args.platform == 'all' or args.platform =='simulator') and not configure_build_and_install(args.source_directory,args.install_directory,True):
        print "Error during the build and installation of the simulator version."
    if (args.platform == 'all' or args.platform =='device') and not configure_build_and_install(args.source_directory,args.install_directory,False):
        print "Error during the build and installation of the simulator version."

    os.chdir(cwd)
 
if __name__ == "__main__" :
    main()
