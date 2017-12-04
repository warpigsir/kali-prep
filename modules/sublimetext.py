#!/usr/bin/env python
import subprocess
import os

import modules.shared as shared

def install_dependencies():
    shared.install_from_apt("apt-transport-https")
        
def install():
    # install java
    if os.path.isfile("/etc/apt/sources.list.d/sublime-text.list"):
        print "sublime-text already in apt sources."
        subprocess.call(["apt-get", "update"])
        shared.install_from_apt("sublime-text")
    else: # add sources and then install java
        source_list = open("/etc/apt/sources.list.d/sublime-text.list", "w")
        source_list.write("deb https://download.sublimetext.com/ apt/stable/\n")
        source_list.close()
        shared.download_from_http("https://download.sublimetext.com/sublimehq-pub.gpg")
        subprocess.call(["apt-key", "add", shared.INSTALL_DIR + "sublimehq-pub.gpg"])
        subprocess.call(["apt-get", "update"])
        shared.install_from_apt("sublime-text")

def test():
    if(os.path.exists("/etc/apt/sources.list.d/sublime-text.list")):
        pass
    else:
        return "Sublime text not present in apt sources list."

    # test if sublime-text and apt-transport-https is installed
    installs = ["sublime-text", "apt-transport-https"]
    for item in installs:
        if(shared.is_installed(item)):
            pass
        else:
            return "Package %s not installed" % item

def print_instructions():
    return "Run Sublimetext with: subl \"file\""

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