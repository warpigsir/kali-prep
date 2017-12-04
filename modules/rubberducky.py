#!/usr/bin/env python
import os

import modules.shared as shared

def install_dependencies():
    pass
        
def install():
    #create rubberducky dir and download duckencoder.jar
    rubberducky_dir = shared.INSTALL_DIR + "rubberducky/"
    if not os.path.exists(rubberducky_dir):
        os.makedirs(rubberducky_dir)
        shared.download_from_http("https://github.com/hak5darren/USB-Rubber-Ducky/raw/master/duckencoder.jar")
        os.rename(shared.INSTALL_DIR + "duckencoder.jar", rubberducky_dir + "duckencoder.jar")

def test():
    if(os.path.exists(shared.INSTALL_DIR + "rubberducky/duckencoder.jar")):
        pass
    else:
        return "Rubberducky not installed"

def print_instructions():
    return "Howto: https://github.com/hak5darren/USB-Rubber-Ducky"

def runall():
    if(shared.DEBUG):
        install_dependencies()
        install()
        failed_tests = test()
        instructions = print_instructions()
    else:
        # supress output from this point on
        with shared.suppress_stdout_stderr():
            install_dependencies()
            install()
            failed_tests = test()
            instructions = print_instructions()
    return instructions, failed_tests