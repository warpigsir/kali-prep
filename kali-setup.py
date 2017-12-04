#!/usr/bin/env python
import subprocess
import os
import getpass
import sys
import getopt

# Our own modules, put your install script in modules and add to __init.py__
from modules import *

def setup_script():
    """
    Setup for this install script to run properly, ie. create INSTALL_DIR
    """
    # supress output from this point on
    with shared.suppress_stdout_stderr():
        #all installations get dumped here.
        shared.INSTALL_DIR = "/root/installs/"
        if not os.path.exists(shared.INSTALL_DIR):
            os.makedirs(shared.INSTALL_DIR)

def update_kali():
    """
    Update and dist-upgrade Kali, answering default to all prompts.
    """
    print "Updating and upgrading Kali..."
    # supress output from this point on
    with shared.suppress_stdout_stderr():
        os.environ["DEBIAN_FRONTEND"] = "noninteractive" # https://unix.stackexchange.com/questions/107194/make-apt-get-update-and-upgrade-automate-and-unattended
        subprocess.call(["apt-get", "update"])
        subprocess.call(["apt-get", "-o", "Dpkg::Options::=\"--force-confdef\" ,Dpkg::Options::=\"--force-confold\""])
        subprocess.call(["apt-get", "dist-upgrade", "-y"])
        subprocess.call("clear",shell=True)

def install_modules():
    """
    Runs the modules listed below (and any extra modules from command line args).
    Each module is responsible for installation and testing.
    Output is shown to indicate if module test cases were successful.
    """
    # default list of modules
    DISPATCHER = {"aptpackages": aptpackages.runall,
        "powershellscripts": powershellscripts.runall,
        "cheatsheets": cheatsheets.runall,
        "rubberducky": rubberducky.runall,
        "sublimetext": sublimetext.runall,
        "empire": empire.runall,
        "mailsniper": mailsniper.runall}

    # add extra modules at runtime if needed.
    if("modules" in locals()):
        for m in modules:
            DISPATCHER[m] = m + ".runall"

    # for each item in dispatcher (module), run it and see if the modules tests returned success or not.
    for fname,f in DISPATCHER.iteritems():
        result = f()
        
        instructions, install_status = result

        if(install_status):
            print u"\u001b[41;1m ERROR: {} \u001b[0m  Error message: {}  ".format(fname,install_status)
        else:
            print u"\u001b[42;1m COMPLETE \u001b[48;5;240m {} \u001b[0m {} ".format(fname, instructions)

def usage():
    print "Usage: ./kali-setup.py"
    print "Usage: ./kali-setup.py --modules=\"module name\",\"other module name\""

def main(argv):
    # get command line parameters (options)
    # getopt help: http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hm:d",["modules="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()                     
            sys.exit()
        elif opt in ("-d", "--debug"):
            shared.DEBUG=True
            print u"\u001b[43;1m DEBUGGING OUTPUT SHOWN \u001b[0m"
        elif opt in ("-m", "--modules"):
            # split module args at comma
            modules = [x.strip() for x in arg.split(',')]

    # display ASCII art
    shared.print_ascii_art()

    setup_script()
    update_kali()
    install_modules()
    
if __name__ == "__main__":
    main(sys.argv[1:])