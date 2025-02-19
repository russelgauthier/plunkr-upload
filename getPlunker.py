#!/usr/bin/python3
import sys
import subprocess
import os

if len(sys.argv) not in (2, 5, 6):
    print("Error: specify the plunkerID. If upload desired include add FTP hostname, FTP username, FTP password and optionally the FTP dir")
    exit(-1)

plunkrId = sys.argv[1]

toUpload = False
if len(sys.argv) >= 5:
    (ftp_hostname, ftp_username, ftp_password) = sys.argv[2:5]
    toUpload = True

ftp_dir = ""
if len(sys.argv) == 6:
    ftp_dir = sys.argv[5]

tmpFileName = "%s.html" % plunkrId
ftp_template_name = "ftp_upload_template.txt"

def runCmd(cmd):
    p = None
    res = subprocess.call([cmd], shell=True)
    return res


def downloadFile(fileName, plunkrId):
    assetStart = 'wget "http://run.plnkr.co/plunks/%s/' % (plunkrId)
    downloadCmd = assetStart + '%s" -O %s' % (fileName, os.path.join(plunkrId, fileName))
    print(downloadCmd)
    runCmd(downloadCmd)

def getFiles(plunkrId):
    cmdStart = 'wget "http://embed.plnkr.co/%s/preview" -O %s' % (plunkrId, tmpFileName)
    runCmd(cmdStart)

    if not os.path.isdir(plunkrId):
        os.mkdir(plunkrId)

    fullFile = ""
    for line in open(tmpFileName):
        fullFile += line

    parts = fullFile.split("embed.file({filename:")
    for part in parts[1:]:
        currFileName = part.split("'})\">")[0].split(" '")[1].strip()
    
        fileParts = currFileName.split(".")
        if fileParts[-1] == "scss":
            cssFile = ".".join(fileParts[:-1]) + ".css"
            downloadFile(cssFile, plunkrId)
        downloadFile(currFileName, plunkrId)
    os.remove(tmpFileName)

def getValidFiles(plunkrId):
    filesSrc = []
    filesDest = []
    for (_path, _dirs, _files) in os.walk(plunkrId):
        for _file in _files:
            currFile = "/".join([_path, _file])
            if len(currFile.split("/")) <= 2:
                filesSrc += [currFile]
                filesDest += [_file]
    return (filesSrc, filesDest)

def uploadFiles(plunkrId):
    (filesSrc, filesDest) = getValidFiles(plunkrId)
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
        elif currLine == "cd $WEBDIR":
            if len(ftp_dir) > 0:
                currLine = "cd %s" % ftp_dir
            else:
                currLine = ""

        contents += currLine + "\n"
    print(contents)
    runCmd(contents)
    print("Upload complete")


getFiles(plunkrId)
if toUpload:
    uploadFiles(plunkrId)
