#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANOPTOSYNC_UPDATER:

This is a simple script that keeps up to date [PanoptoSync](https://gitlab.com/Microeinstein/panopto-sync).
> The tool that downloads UniVR lessons

PanoptoSync was coded by Microeinstein (https://gitlab.com/Microeinstein)
Update tool was coded by mario33881 (https://github.com/mario33881)

PanoptoSync was released with the "GNU General Public License v3.0":
You can find its license files here: https://gitlab.com/Microeinstein/panopto-sync/-/blob/master/LICENSE

Gitlab repository of PanoptoSync: https://gitlab.com/Microeinstein/panopto-sync
Github repository of this update tool: https://github.com/mario33881/panoptosync_updater
"""

__author__ = "Zenaro Stefano"
__version__ = "2021-08-18 01_01"

import os
import datetime
import zipfile
import json
import typing
import urllib.error
import urllib.parse
import urllib.request
from email.message import Message
import traceback
import shutil

boold = False
if boold:
    import time

panoptosync_url = "https://gitlab.com/api/v4/projects/18406702/repository/commits"
download_url = "https://gitlab.com/Microeinstein/panopto-sync/-/archive/master/panopto-sync-master.zip"
script_dir = os.path.dirname(os.path.realpath(__file__))


def show_intro_msg():
    """Show intro message."""
    print("PanoptoSync was coded by Microeinstein (https://gitlab.com/Microeinstein)")
    print("Update tool was coded by mario33881 (https://github.com/mario33881)")
    print("")
    print("PanoptoSync was released with the \"GNU General Public License v3.0\":")
    print("You can find its license files here: https://gitlab.com/Microeinstein/panopto-sync/-/blob/master/LICENSE")
    print("or inside this current folder (the license file will be downloaded together with PanoptoSync)")
    print("=" * 30)
    print("Checking if an update is available...")
    

def show_error_msg(err):
    """
    Show the error and invite the user to report it on Github.

    :param Exception err: error
    """
    print("-" * 30)
    print("An unexpected error occured:", str(err))
    print("```")
    print("Traceback:\n")
    traceback.print_tb(err.__traceback__)
    print("")
    type_of_error = type(err)
    print(type_of_error.__name__, ": " + str(err))
    print("```")
    print("Please copy and paste this full message (from 'PanoptoSync was coded by Microeinstein' to the next line) and report it here: https://github.com/mario33881/panoptosync_updater/issues")
    print("> After signing up/logging in follow this tutorial: https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue#creating-an-issue-from-a-repository")
    print("\nNOTE: This error was thrown by the Update tool. PanoptoSync should still work!")


def seconds_between(first_time, later_time):
    """
    Returns the seconds between two dates

    :param str first_time: first date
    :param str later_time: later date
    :ret int: seconds between the two dates
    """
    first_time = datetime.datetime.fromisoformat(first_time)
    later_time = datetime.datetime.fromisoformat(later_time)
    difference = later_time - first_time
    return difference.total_seconds()


class Response(typing.NamedTuple):
    body: str
    headers: Message
    status: int
    error_count: int = 0

    def json(self) -> typing.Any:
        """
        Decode body's JSON.

        Returns:
            Pythonic representation of the JSON object
        """
        try:
            output = json.loads(self.body)
        except json.JSONDecodeError:
            output = ""
        return output


def request(
    url: str,
    data: dict = None,
    params: dict = None,
    headers: dict = None,
    method: str = "GET",
    data_as_json: bool = True,
    error_count: int = 0,
) -> Response:
    """
    Make a request without non-standard libraries
    """
    if not url.casefold().startswith("http"):
        raise urllib.error.URLError("Incorrect and possibly insecure protocol in url")
    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers = {"Accept": "application/json", **headers}

    if method == "GET":
        params = {**params, **data}
        data = None

    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True, safe="/")

    if data:
        if data_as_json:
            request_data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json; charset=UTF-8"
        else:
            request_data = urllib.parse.urlencode(data).encode()

    httprequest = urllib.request.Request(
        url, data=request_data, headers=headers, method=method
    )

    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response = Response(
                headers=httpresponse.headers,
                status=httpresponse.status,
                body=httpresponse.read().decode(
                    httpresponse.headers.get_content_charset("utf-8")
                ),
            )
    except urllib.error.HTTPError as e:
        response = Response(
            body=str(e.reason),
            headers=e.headers,
            status=e.code,
            error_count=error_count + 1,
        )

    return response


def download_extract_zip(url, dest):
    print("Downloading zip file...")
    if boold:
        time.sleep(5)
    urllib.request.urlretrieve(url, os.path.join(dest, "tmp_zipfile.zip"))

    # extract it
    print("Extracting zip file...")
    if boold:
        time.sleep(5)
    with zipfile.ZipFile(os.path.join(dest, "tmp_zipfile.zip"), 'r') as zip_ref:
        zip_ref.extractall(dest)

    # delete the zip file
    print("Deleting zip file...")
    if boold:
        time.sleep(5)
    os.remove(os.path.join(dest, "tmp_zipfile.zip"))


def download_and_setup():
    """
    Download new files, delete old files and replace them with the new files.
    """
    download_extract_zip(download_url, script_dir)

    # copy this script inside the new version's folder
    print("Copying this script to the new folder...")
    if boold:
        time.sleep(5)
    shutil.copyfile(os.path.join(script_dir, "ps_updater.py"), os.path.join(script_dir, "panopto-sync-master", "ps_updater.py"))

    print("Copying id and cookies files (if present)...")
    if boold:
        time.sleep(5)
    
    if os.path.isfile(os.path.join(script_dir, "default.id")):
        shutil.copyfile(os.path.join(script_dir, "default.id"), os.path.join(script_dir, "panopto-sync-master", "default.id"))
    
    if os.path.isfile(os.path.join(script_dir, "default.cookies")):
        shutil.copyfile(os.path.join(script_dir, "default.cookies"), os.path.join(script_dir, "panopto-sync-master", "default.cookies"))

    # delete __pycache__ folder
    print("Deleting __pycache__ folder...")
    if boold:
        time.sleep(5)

    try:
        shutil.rmtree((os.path.join(script_dir, "__pycache__")))
    except FileNotFoundError:
        # if it can't find the folder, no problem: ignore it
        pass

    # delete files in this folder
    print("Deleting old files in this folder...")
    if boold:
        time.sleep(5)

    for element in os.listdir(script_dir):
        if os.path.isfile(element):
            if os.path.join(script_dir, element) != os.path.join(script_dir, "ps_updater.py"):
                os.remove(os.path.join(script_dir, element))

    # Move all the newfiles to this parent directory
    print("Moving new files to this folder...")
    if boold:
        time.sleep(5)

    source = os.path.join(script_dir, "panopto-sync-master")
    destination = script_dir
    files_list = os.listdir(source)
    for file in files_list:
        if boold:
            print("Moving file:", file)
        try:
            shutil.move(os.path.join(source, file), destination)
        except shutil.Error as e:
            if not "already exists" in str(e):
                raise e

    # delete the now empty folder
    print("Deleting empty 'new' folder...")
    if boold:
        time.sleep(5)

    shutil.rmtree(source)

    # create a file that contains the latest commit date
    print("Creating file with the updated commit date...")

    with open(os.path.join(script_dir, "latest_commit_date.txt"), "w") as f:
        f.write(latest_commit_date)
    
    print("\nDone.\n")


if __name__ == "__main__":

    # check if panoptoSync is installed
    not_installed = False
    if not os.path.isfile(os.path.join(script_dir, "panoptoSync.py")):
        not_installed = True

    show_intro_msg()

    try:
        # get info from api
        r = request(panoptosync_url)

        if r.status == 200:
            # get the latest commit data and extract its date
            json_data = r.json()
            latest_commit = json_data[0]
            latest_commit_date = latest_commit["created_at"]

            # extract the current commit date
            if os.path.isfile(os.path.join(script_dir, "latest_commit_date.txt")) or not_installed:
                if not_installed:
                    print("Couldn't find PanoptoSync, downloading it now...")
                    download_and_setup()
                else:
                    # get current version's date of commit
                    with open(os.path.join(script_dir, "latest_commit_date.txt"), "r") as f:
                        current = f.read().strip()
                    
                    # if a commit has been uploaded at least 30 seconds ago (safer than > 0)... download PanoptoSync
                    if boold:
                        print("The difference in seconds between these versions are: ", seconds_between(current, latest_commit_date))

                    if seconds_between(current, latest_commit_date) > 30 or boold:
                        print("A new PanoptoSync update is available... downloading it...")
                        download_and_setup()
                    else:
                        print("There are no PanoptoSync updates available")
            else:
                # this is the first time that this script was executed
                with open(os.path.join(script_dir, "latest_commit_date.txt"), "w") as f:
                    current = f.write(latest_commit_date)
                print("Created version file. There seem to be no PanoptoSync updates available")
        else:
            # for some reason the request returned something other than status 200
            raise Exception("Couldn't retrive updates information at this url: '" + panoptosync_url + "'")
    
    except Exception as e:
        # show the error and invite the user to report it
        show_error_msg(e)
    
    print("=" * 30)
    print("")
