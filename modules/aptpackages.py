#!/usr/bin/env python
import modules.shared as shared

INSTALLS = ["ftp", "gobuster", "brasero", "bloodhound", "xul-ext-foxyproxy-standard", "virtualbox"]

def install_dependencies():
    pass

def install():
    for item in INSTALLS:
        if(shared.is_installed(item)):
            pass
        else:
            shared.install_from_apt(item)

def test():
    for item in INSTALLS:
        if(shared.is_installed(item)):
            pass
        else:
            return "Package %s not installed" % item

def print_instructions():
    return INSTALLS

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