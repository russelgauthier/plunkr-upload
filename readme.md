Purpose
=======
Downloads all files for applicable plunkr project into a directory named after the plunkerId
Uploads files if FTP information is specified (hostname, username, password)
For uploads the webdir can be specified as the last argument, otherwise files are uploaded to the user's home directory

Requirements
============
- Python >= 3

Instructions
============
1. Go into run.sh and enter your:
     - PlunkrID for your project (e.g. http://plnkr.co/edit/5cQjKj41NIVAPUcECC6K?p=preview => 5cQjKj41NIVAPUcECC6K)
2. Enter your FTP information in run.sh if you want downloaded files to be uploaded via FTP:
     - FTP_HOSTNAME
     - FTP_USERNAME
     - FTP_PASSWORD
     - FTP_DIR (Not required. If not specified uploads are done to the user's home directory)
2. chmod u+x run.sh getPlunker.py
3. ./run.sh and the files will be downloaded and the files will be uploaded through FTP

Nota Bene
=========
1. Previous files are NOT deleted in the directory remotely or locally. That would have to be done manually, if desired
2. git doesn't auto-commit, as it would be hard to determine when commits would be desired, as opposed to just attempts to upload files

