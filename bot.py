import os
import time
import re
import io
import subprocess
from slackclient import SlackClient
from roshi import Manga, Chapter
import pickle


SERIES = ['One Piece 2']


def get_log():
    log = {}

    if(not os.path.exists("chapter_log.pkl")):
        return log
    
    with open("chapter_log.pkl", "rb") as file:
        log = pickle.load(file)
    
    return log


def save_log(log):
    with open("chapter_log.pkl", "wb") as file:
        pickle.dump(log, file)


def send_chapter_to_slack(filename, series, chaptername):
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    print(slack_token)
    slack_client = SlackClient(slack_token)

    response = slack_client.api_call(
        "chat.postMessage",
        channel="CBYUFSUFQ",
        text="New {} chapter. It will be uploaded shortly. :zoro:".format(series)
    )
    
    with open('{}.cbz'.format(filename), 'rb') as f:
        response = slack_client.api_call(
            'files.upload',
            channels='CBYUFSUFQ',
            file=io.BytesIO(f.read()),
            filename="{}".format(filename),
            title="{}".format(chaptername)
        )

        print(response)


def check_for_chapters():
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
        check_for_chapters()
        time.sleep(300)
    
