#!/usr/bin/python3
import sys
import subprocess
import shutil
import os

if len(sys.argv) != 5:
    print("Error: 4 arguments required -> plunkerID, FTP hostname, FTP username, FTP password")
    exit(-1)

(plunkrId, ftp_hostname, ftp_username, ftp_password) = sys.argv[1:]
tmpFileName = "%s.html" % plunkrId
ftp_template_name = "ftp_upload_template.txt"
#ftp_hostname = "ftp.movadamedia.com"
#ftp_username = "russelg"
#ftp_password = "Password1!"

def runCmd(cmd):
    p = None
    res = subprocess.call([cmd], shell=True)
    return res


def getFiles(plunkrId):
    cmdStart = 'wget "http://embed.plnkr.co/%s/preview" -O %s' % (plunkrId, tmpFileName)
    assetStart = 'wget "http://run.plnkr.co/plunks/%s/' % (plunkrId)

    runCmd(cmdStart)

    if not os.path.isdir(plunkrId):
        os.mkdir(plunkrId)

    fullFile = ""
    for line in open(tmpFileName):
        fullFile += line

    parts = fullFile.split("embed.file({filename:")
    for part in parts[1:]:
        currFileName = part.split("'})\">")[0].split(" '")[1].strip()
    
        downloadCmd = assetStart + '%s" -O %s' % (currFileName, os.path.join(plunkrId, currFileName))
        runCmd(downloadCmd)
    
    os.remove(tmpFileName)

def uploadFiles(plunkrId):
    filesSrc = []
    filesDest = []
    for (_path, _dirs, _files) in os.walk(plunkrId):
        for _file in _files:
            currFile = os.path.join(os.getcwd(), "/".join([_path, _file]))
            filesSrc += [currFile]
            filesDest += [_file]

    print("Uploading files...")
    contents = ""
    for line in open(ftp_template_name):
        currLine = line.strip()
        currLine = currLine.replace("$USER", ftp_username).replace("$PASSWD", ftp_password).replace("$HOST", ftp_hostname)

        if currLine == "put $FILE":
            currLine = ""
            
            i = 0
            for fileSrc in filesSrc:
                currLine += "put %s %s\n" % (fileSrc, filesDest[i])

                i += 1
        contents += currLine + "\n"
    runCmd(contents)
getFiles(plunkrId)
uploadFiles(plunkrId)
