#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import tarfile
import zipfile
import urllib
from contextlib import contextmanager
import sys
import os
import httplib
from time import sleep

DEBUG = False
INSTALL_DIR = ""

def print_ascii_art():
    """
    Prints beautiful ascii art.
    """
    f = open("ascii.txt")
    for line in f:
        print line,
    f.close()

def get_http_status_code(host, path="/"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except StandardError:
        return None

# Define a context manager to suppress stdout and stderr.
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)

def download_from_http(url):
    """
    Downloads a file, using HTTP, to INSTALL_DIR
    """
    filename = url.split('/')[-1]
    print filename
    urllib.urlretrieve(url, INSTALL_DIR + filename)

def install_from_apt(package_name):
    subprocess.call(["apt-get", "-y", "install", package_name])

def is_installed(package_name):
    """
    Check if package is installed via dpkg.

    Equivalent to running "dpkg -s package_name" from command line.

    Parameters
    ----------
    package_name : str
        Name of package to check install status of.

    Returns
    ----------
    bool
        Returns True if package is installed, otherwise returns False
        
    """
    proc = subprocess.Popen(["dpkg", "-s", package_name], stdout=subprocess.PIPE)
    result = proc.stdout.read()
    if "Status: install ok installed" in result:
        return True
    else:
        return False

def unpack(filename):
    """
    Depending on filename will attempt to unpack (using untar or unzip) file to INSTALL_DIR.

    Parameters
    ----------
    filename : str
        Name and path of file to unpack.

    Returns
    ----------
    bool
        Returns True if filename is correct and attempted to unpack, otherwise returns False 
    """
    if (filename.endswith("tar.gz")) or (filename.endswith("tgz")):
        tar = tarfile.open(filename)
        tar.extractall(INSTALL_DIR)
        tar.close()
        return True
    elif (filename.endswith("zip")):
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall(INSTALL_DIR)
        zip_ref.close()
        return True
    else:
        print "Not a tar.gz or .tgz file: '%s '" % filename
        return False