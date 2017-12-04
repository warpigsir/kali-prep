#!/usr/bin/env python
import subprocess
import os

import modules.shared as shared

def install_dependencies():
    """
    Installs docker
    
    Reference: https://docs.docker.com/engine/installation/linux/docker-ce/debian/#install-docker-ce-1
    """
    with shared.suppress_stdout_stderr():
        installs = ["apt-transport-https", "ca-certificates", "curl", "software-properties-common"]
        for item in installs:
            if(shared.is_installed(item)):
                pass
            else:
                shared.install_from_apt(item)

        # download key
        shared.download_from_http("https://download.docker.com/linux/ubuntu/gpg")
        subprocess.call(["apt-key", "add", shared.INSTALL_DIR + "gpg"])

        # add to apt sources
        source_list = open("/etc/apt/sources.list.d/docker.list", "w")
        source_list.write("deb [arch=amd64] https://download.docker.com/linux/debian wheezy stable\n")
        source_list.close()
        
        #install docker
        subprocess.call(["apt-get", "update"])
        subprocess.call(["apt-get", "-y", "install", "docker-ce"])

def install():
    """
    Installs docker
    
    Reference: https://hub.docker.com/r/tvelocity/etherpad-lite/
    """
    with shared.suppress_stdout_stderr():
        subprocess.call(["docker", "network", "create", "ep_network"])
        subprocess.call(["docker", "run", "-d", "--network", "ep_network", "-e", "MYSQL_ROOT_PASSWORD=password", "--name", "ep_mysql", "mysql"])
        subprocess.call(["docker", "run", "-d", "--network", "ep_network", "-e", "ETHERPAD_DB_HOST=ep_mysql", "-e", "ETHERPAD_DB_PASSWORD=password", "-p", "9001:9001", "tvelocity/etherpad-lite"])

def test():
    
    if(os.path.exists("/etc/apt/sources.list.d/docker.list")):
        pass
    else:
        return "Docker not present in apt sources list."
    
    # are prereqs installed?
    installs = ["apt-transport-https", "ca-certificates", "curl", "software-properties-common", "docker-ce"]
    for item in installs:
        if(shared.is_installed(item)):
            pass
        else:
            return "Package %s not installed" % item

    # is docker installed?
    proc = subprocess.Popen(["docker", "run", "hello-world"], stdout=subprocess.PIPE)
    result = proc.stdout.read()
    if "Hello from Docker!" in result:
        pass
    else:
        return "Docker not installed."
        

    # is etherpad running on http://127.0.0.1:9001/ ?
    if(shared.get_http_status_code("localhost:9001") == 200):
        pass
    else:
        return "Etherpad docker image not installed."

def print_instructions():
    return "Etherpad docker running on: http://127.0.0.1:9001/"

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