#!/usr/bin/env python
import subprocess
import os

import modules.shared as shared

def install_dependencies():
    pass
        
def install():
    subprocess.call(["git", "clone", "https://github.com/dafthack/MailSniper.git", shared.INSTALL_DIR + "MailSniper"])

def test():
    #test Empire is downloaded to correct location
    if(os.path.exists(shared.INSTALL_DIR + "MailSniper")):
        pass
    else:
        return "MailSniper not installed."


def print_instructions():
    return "Import /root/installs/MailSniper/MailSniper.ps1 + powershell Invoke-SelfSearch -Mailbox current-user@domain.com"

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