#!/usr/bin/env python
import subprocess
import os

import modules.shared as shared

def install_dependencies():
    pass
        
def install():
    if(os.path.exists(shared.INSTALL_DIR + "PowerSploit-dev")):
        pass
    else:
        shared.download_from_http("https://github.com/PowerShellMafia/PowerSploit/archive/dev.zip")
        shared.unpack(shared.INSTALL_DIR + "dev.zip")
    if(os.path.exists(shared.INSTALL_DIR + "PowerUpSQL")):
        pass
    else:
        subprocess.call(["git", "clone", "https://github.com/NetSPI/PowerUpSQL.git", shared.INSTALL_DIR + "PowerUpSQL"])

def test():
    #test PowerSploit and PowerUpSQL is downloaded to correct location
    if(os.path.exists(shared.INSTALL_DIR + "PowerSploit-dev")) and (os.path.exists(shared.INSTALL_DIR + "PowerUpSQL")):
        pass
    else:
        return "Powershell scripts not installed correctly."


def print_instructions():
    return "Powershell scripts located in: " + shared.INSTALL_DIR

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