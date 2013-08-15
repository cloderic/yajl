#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import subprocess
import shutil

defaultSourceDirectory = os.path.abspath("..")
defaultBuildDirectory = os.path.abspath("./mac/")
defaultInstallDirectory = os.path.abspath("../install/mac")

def configure_build_and_install(sources_directory, install_directory):
    returnStatus = subprocess.call([
        "cmake", 
        "-DCMAKE_INSTALL_PREFIX={}".format(install_directory),
        "-GXcode",
        "{}".format(sources_directory)])
    
    if returnStatus != 0:
        return False
    
    return do_build_and_install("Debug") and do_build_and_install("Release")

def do_build_and_install(configuration):
    returnStatus = subprocess.call([
        "xcodebuild", 
        "-target", "install",
        "-configuration", "{}".format(configuration)]);
    if returnStatus != 0:
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description="Building and installing YAJL for mac os")
    parser.add_argument("--source_directory", help="Source directory (default is %(default)s)", default=defaultSourceDirectory)
    parser.add_argument("--build_directory", help="Build directory (default is %(default)s)", default=defaultBuildDirectory)
    parser.add_argument("--install_directory", help="Install directory (default is %(default)s)", default=defaultInstallDirectory)
    args = parser.parse_args()

    cwd = os.getcwd()
    
    if not os.path.exists(args.build_directory):
    	os.mkdir(args.build_directory)
    os.chdir(args.build_directory)

    if not configure_build_and_install(args.source_directory,args.install_directory):
        print "Error during the build and installation."

    os.chdir(cwd)
 
if __name__ == "__main__" :
    main()
