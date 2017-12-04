#!/usr/bin/env python
import subprocess
import os

import modules.shared as shared

CHEATSHEET_DIR = "/root/cheatsheets/"

def install_dependencies():
    pass
        
def install():
    #create cheatsheet dir
    if not os.path.exists(CHEATSHEET_DIR):
        os.makedirs(CHEATSHEET_DIR)

    cheatsheets = ["https://github.com/HarmJ0y/CheatSheets/raw/master/Beacon.pdf", "https://github.com/HarmJ0y/CheatSheets/raw/master/Empire.pdf", "https://github.com/HarmJ0y/CheatSheets/raw/master/PowerSploit.pdf", "https://github.com/HarmJ0y/CheatSheets/raw/master/PowerUp.pdf", "https://github.com/HarmJ0y/CheatSheets/raw/master/PowerView.pdf"]

    for item in cheatsheets:
        filename = item.split('/')[-1]
        if(os.path.exists(CHEATSHEET_DIR + filename)):
            pass
        else:
            shared.download_from_http(item)
            os.rename(shared.INSTALL_DIR + filename, CHEATSHEET_DIR + filename)

    if(os.path.exists(CHEATSHEET_DIR + "PowerUpSQL")):
        pass
    else:
        subprocess.call(["git", "clone", "https://github.com/NetSPI/PowerUpSQL.wiki.git", CHEATSHEET_DIR + "PowerUpSQL"])

def test():
    #test if cheatsheet dir exists and the correct files are present
    cheatsheets = ["https://github.com/HarmJ0y/CheatSheets/raw/master/Beacon.pdf", "https://github.com/HarmJ0y/CheatSheets/raw/master/Empire.pdf", "https://github.com/HarmJ0y/CheatSheets/raw/master/PowerSploit.pdf", "https://github.com/HarmJ0y/CheatSheets/raw/master/PowerUp.pdf", "https://github.com/HarmJ0y/CheatSheets/raw/master/PowerView.pdf"]

    for item in cheatsheets:
        filename = item.split('/')[-1]
        if(os.path.exists(CHEATSHEET_DIR + filename)):
            pass
        else:
            return "Powershell scripts not installed"

def print_instructions():
    return "Cheatsheets located in: " + CHEATSHEET_DIR

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