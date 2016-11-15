#!/usr/bin/env python
# Docker hosts configuration script
import sys
import subprocess
import optparse
import commands

# VARIABLES
defaultRoute= "/etc/hosts"
defaultDM= "default"


# FUNCTIONS

# get users answer to some message
def getUsersYesNo(msg):
    while True:
        answ = raw_input(msg +" (y/n): ").lower()
        if answ == "n":
            return False

        elif (answ == "y"):
            return True

# check if a string is inside a file
def isStringInFile(str,path):
    if str in open(path).read():
         return True
    return False
def hasArraySubstringFromString(array,string):
    for str in array:
        if str in string :
            return True
    return False

def writeFiles(override,path,ip,domains):
    # create backup file
    backupPath = path + ".old"

    tempPath = "/tmp/etc_hosts.tmp"

    print("[Config]: Writing files...")
    lines = []
    # read file and comment conflicts
    with open(path,"r") as infile:
        for line in infile:
            # if ip or domain exists in file that line is not stored
            if not ((ip in line) or hasArraySubstringFromString(domains,line)):
                lines.append(line)
    # write file
    with open(tempPath, 'wd') as outfile:
        for line in lines:
            outfile.write(line)
        # write ip and domains
        outfile.write(ip + "  " + " ".join(domains) + "\n")

    subprocess.call("sudo mv " + path + " " + backupPath, shell=True)
    # move temporary file to path
    subprocess.call("sudo mv " + tempPath + " " + path, shell=True)
    print("[Write]: Files written..."+u'\u2713')
    # ask about keepng backup file
    if not override:
        if not getUsersYesNo("Do you want to create a backup file .old?"):
            subprocess.call("sudo rm " + backupPath, shell=True)
    else:
        subprocess.call("sudo rm " + backupPath, shell=True)

    # give same permissions as before to created file
    subprocess.call("sudo chmod 644 " + path, shell=True)
    print("[Write]: Restoring permissions..." + u'\u2713')


def checkIpDomains(ip,domains,path,override):
    print("[Config]: Checking hosts file...")
    # check if ip is allready assigned
    if isStringInFile(ip,path):
        if not override:
            if not getUsersYesNo("IP <" + ip + "> is allready assigned to a domain,\ndo you want to override it?"):
                print("[Check]: operation cancelled")
                sys.exit(1)
    else:
        print("[Check]: IP not used " + u'\u2713')


    # check if domains are allready assigned
    for domain in domains:
        if isStringInFile(domain,path):
            if not override:
                if not getUsersYesNo("Domain <" + domain + "> is allready assigned to an IP,\ndo you want to override it?"):
                    print("[Check]: operation cancelled")
                    sys.exit(1)
        else:
            print("[Check]: Domain " + domain + " not used " + u'\u2713')

    # check if user wants to override srings
    writeFiles(override,path,ip,domains)

def splitDomains(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))



# OPTIONS
parser = optparse.OptionParser()

parser.add_option('-r', '--route', dest='route', help='Hosts alternative Path')
parser.add_option('-i', '--ip', dest='dmIp', help='Custom IP address')
parser.add_option('-d', '--domain', dest='domains', type="string", help="Custom domain or domain, f.e -d mydomain.com,mydomain2.com", action='callback',
callback=splitDomains)
parser.add_option('-n', '--name', dest='dmName', help="docker-machine's name to configure, by default docker-machine calls it <default>")
parser.add_option('-o', action="store_true", help="override strings found in file", dest="override")


(options, args) = parser.parse_args()

if options.route is None:
    options.route = defaultRoute

if options.domains is None:
    while True:
        answ = raw_input("Enter a domain name: ")
        if answ != "":
            options.domains = [answ]
            break

if options.dmIp is None:
    # get docker machine alternative name
    if options.dmName is None:
        options.dmName = defaultDM

    # get docker-machine ip
    p = subprocess.Popen(["docker-machine","ip",options.dmName], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #p = subprocess.Popen(["rm","python-server"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    options.dmIp, err = p.communicate()
    # check any errors and missing values
    if ((options.dmIp.strip() == "") or (err != "")):
        print("Error getting docker-machine's IP, is docker-machine " + options.dmName + " running?")
        sys.exit(1)
    print("[Config]: docker-machine's  IP <" + options.dmIp.strip() + ">")


# CODE
print("DOMAINS")
for domain in options.domains:
    print domain
checkIpDomains(options.dmIp.strip(),options.domains,options.route,options.override);
