# PANOPTOSYNC_UPDATER

[![Unit Tests](https://github.com/mario33881/panoptosync_updater/actions/workflows/unittest.yml/badge.svg)](https://github.com/mario33881/panoptosync_updater/actions/workflows/unittest.yml)

This is a simple script that keeps up to date [PanoptoSync](https://gitlab.com/Microeinstein/panopto-sync).
> The tool that downloads UniVR lessons

PanoptoSync was coded by Microeinstein (https://gitlab.com/Microeinstein)

This update tool was coded by mario33881 (https://github.com/mario33881)
 
> Gitlab repository of PanoptoSync: https://gitlab.com/Microeinstein/panopto-sync
>
> Github repository of this update tool: https://github.com/mario33881/panoptosync_updater

PanoptoSync was released with the "GNU General Public License v3.0". You can find its license files here: 
* https://gitlab.com/Microeinstein/panopto-sync/-/blob/master/LICENSE
* or inside the folder you execute this script in (the license file will be downloaded together with PanoptoSync)

## Description

This script:
* checks if PanoptoSync is available inside its directory, downloads PanoptoSync if it doesn't find the ```panoptoSync.py``` file and creates a ```latest_commit_date.txt``` file.
    > This script must be placed in the SAME folder as the ```panoptoSync.py``` file

* If the ```latest_commit_date.txt``` file DOES NOT exist it creates it with the latest commit date it can find using the Gitlab API.

    This is the API URL used by this script:
    ```
    https://gitlab.com/api/v4/projects/18406702/repository/commits
    ```
    > ```18406702``` is the project id of [PanoptoSync](https://gitlab.com/Microeinstein/panopto-sync) on Gitlab.

    At this point the script assumes that you are using the latest commit and creates the file for you.

    When you execute this script and PanoptoSync has been modified, this script will find the new version and download it.

* If the ```latest_commit_date.txt``` file exists the script thinks that a new version is available if the new version has been released at least 30 seconds after the currently installed one.
    > This is used instead of "> 0 seconds" to avoid unexpected behaviour if something strange happens with the returned dates of the API. Might never happen...

    > This time might be reduced in the future... 5 seconds could be more than enough

## Usage

Download this script and put it in the same directory as the ```panoptoSync.py``` file.

Execute it manually once in a while to update panoptoSync:

    python3 ps_updater.py

> You can also execute it automatically by creating a batch/shell script that executes this script before panoptoSync or create a cronjob with [cron](https://en.wikipedia.org/wiki/Cron) in Unix-like OSes

Example of batch file (Windows) placed in the same directory as the ```panoptoSync.py``` file:
```bat
@echo off

REM Remember User's current path
set OLDPATH="%cd%"

REM Go inside the panoptoSync folder (same directory as this script)
cd "%~dp0"

REM Execute panoptosync_updater with python (might need to change the python command)
py -3 ps_updater.py

REM Execute panoptoSync using python (might need to change the python command)
REM and pass it all the parameters given to this script
py -3 panoptoSync.py %*

REM Go back to the User's original directory
cd "%OLDPATH%"
```

A *nix equivalent script should work just as fine.

## Found some bugs?
Please, create an issue at this page by clicking the "New Issue" button: https://github.com/mario33881/panoptosync_updater/issues

Pull Requests are also accepted.

## Dependencies

* python 3

> This script was coded to use only the built-in libraries

## Changelog

**2021-08-18 01_01**:

First commit

## Author
Stefano Zenaro ([mario33881](https://github.com/mario33881))