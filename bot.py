#!/usr/bin/python3

import os
import time
import re
import io
import subprocess
from slack import WebClient
from roshi import Manga, Chapter
import json

DEBUG = os.environ.get("DEBUG")
SLACK_CHANNEL = "#roshi"
HISTORY_DIR = ".history"
HISTORY_FILE = "chapter_history.json"
HISTORY_FILE_PATH = os.path.join(HISTORY_DIR, HISTORY_FILE)

SERIES = ['One Piece 2']

if DEBUG == "True":
    SLACK_CHANNEL = "#test"


def init_log_dir():
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)


def get_log():
    log = {}

    if(not os.path.exists(HISTORY_FILE_PATH)):
        return log
    
    with open(HISTORY_FILE_PATH, "r") as file:
        file_content = file.read()
        log = json.loads(file_content)

    return log


def save_log(log):
    with open(HISTORY_FILE_PATH, "w") as file:
        file.write(json.dumps(log))

	
def send_chapter_to_slack(filename, series, chaptername):
    slack_token = os.environ.get('SLACK_BOT_TOKEN')

    slack_client = WebClient(slack_token)

    response = slack_client.chat_postMessage(
        channel=SLACK_CHANNEL,
        text="New {} chapter. It will be uploaded shortly. :zoro:".format(series)
    )

    assert response["ok"]
    
    with open('{}.cbz'.format(filename), 'rb') as f:
        response = slack_client.files_upload(
            channels=SLACK_CHANNEL,
            file=io.BytesIO(f.read()),
            filename="{}.cbz".format(filename),
            title="{}".format(chaptername)
        )

        assert response["ok"]


def check_for_chapters():
    init_log_dir()

    log = get_log()

    for s in SERIES:
        manga_series = Manga(s)
        latest_number, chapter, source = manga_series.get_latest_details()

        logged_chapter_num = log.get(s)
        
        if(logged_chapter_num is not None):
            if(logged_chapter_num >= latest_number):
                print("Skipping Chapter for {}...".format(s))
                continue
        
        print("Getting latest {} chapter...".format(s))
        manga_series.get_latest()
        print("Sending to slack...")
        send_chapter_to_slack(chapter.name, s, "{} - {}".format(s, chapter.name))
        
        log[s] = latest_number
    
    save_log(log)
    

if __name__ == '__main__':
    while True:
        print("Checking for chapters...")
        check_for_chapters()
        print("Sleeping for 30 mins.")
        time.sleep(1800)
    
