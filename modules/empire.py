#!/usr/bin/env python
import subprocess
import os

import modules.shared as shared

def install_dependencies():
    pass
        
def install():
    """
    1. git clone Powershell Empire to /root/installs/Empire
    2. run install.sh with predefined password (STAGING_KEY).
    """
    if os.path.exists(shared.INSTALL_DIR + "Empire"):
        pass
    else:
        # set a staging key for empire, similar to "export STAGING_KEY=cb755a0ff8b48c451f416ef6609577c7"
        os.environ["STAGING_KEY"] = "cb755a0ff8b48c451f416ef6609577c7" # echo -n "affe" | md5sum
        subprocess.call("echo $STAGING_KEY", shell=True)

        subprocess.call(["git", "clone", "https://github.com/EmpireProject/Empire.git", shared.INSTALL_DIR + "Empire"])
        os.chdir(shared.INSTALL_DIR + "Empire/")
        subprocess.call(["./setup/install.sh"])


def test():
    #test Empire is downloaded to correct location
    if(os.path.exists(shared.INSTALL_DIR + "Empire")):
        pass
    else:
        return "Empire not installed"


def print_instructions():
    return "Run PS empire using: cd " + shared.INSTALL_DIR + "Empire/ && ./empire"

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