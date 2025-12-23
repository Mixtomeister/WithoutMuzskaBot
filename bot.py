from dateutil import tz
from dateutil.relativedelta import relativedelta
from datetime import datetime

from bsky_client import BskyClient

import tweepy
import os
import logging

FORMAT = '[%(levelname)s] [%(asctime)s] %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TW_CONSUMER_KEY = os.environ.get('TW_CONSUMER_KEY')
TW_CONSUMER_SECRET = os.environ.get('TW_CONSUMER_SECRET')
TW_ACCESS_KEY = os.environ.get('TW_ACCESS_KEY')
TW_ACCESS_SECRET = os.environ.get('TW_ACCESS_SECRET')

BSKY_USERNAME = os.environ.get('BSKY_USERNAME')
BSKY_APP_PASSWORD = os.environ.get('BSKY_APP_PASSWORD')

MUZSKA_LAST_VIDEO_DATE = os.environ.get('MUZSKA_LAST_VIDEO_DATE')
DATE_FORMAT = os.environ.get('DATE_FORMAT')

TW_POST = os.environ.get('TW_POST') == '1'
BSKY_POST = os.environ.get('BSKY_POST') == '1'

CET = tz.gettz('CET')
MUZSKA_LAST_VIDEO = datetime.strptime(MUZSKA_LAST_VIDEO_DATE, DATE_FORMAT).astimezone(CET)

TWEET_MSG = 'Días sin Muzska:\n\n{last_video}\n\nMuzska te echamos de menos <3'
RELATIVE_MSG = '{num_years} {str_years}, {num_months} {str_months} y {num_days} {str_days}'

def get_relative_time(dt):
    return RELATIVE_MSG.format(num_years=dt.years,
                            str_years='años' if dt.years != 1 else 'año',
                            num_months=dt.months,
                            str_months='meses' if dt.months != 1 else 'mes',
                            num_days=dt.days,
                            str_days='días' if dt.days != 1 else 'día')

def get_post():
    now = datetime.now().astimezone(CET)
    relative_last_video = relativedelta(now, MUZSKA_LAST_VIDEO).normalized()

    return TWEET_MSG.format(last_video=get_relative_time(relative_last_video))

def send_twitter_post(post):
    logger.info("[TW] Login to Twitter...")
    client = tweepy.Client(
        consumer_key=TW_CONSUMER_KEY,
        consumer_secret=TW_CONSUMER_SECRET,
        access_token=TW_ACCESS_KEY,
        access_token_secret=TW_ACCESS_SECRET
    )

    logger.info("[TW] Sending Tweet...")
    client.create_tweet(text=post)
    logger.info('[TW] Tweet sent')

def send_bluesky_post(post):
    logger.info("[BSKY] Login to Bluesky...")

    bsky_client = BskyClient(BSKY_USERNAME, BSKY_APP_PASSWORD)
    bsky_client.create_session()

    logger.info("[BSKY] Sending Post...")

    bsky_client.send_post(post)
    
    logger.info("[BSKY] Post sent")


def lambda_handler(event, context):
    try:
        main()
    except Exception as e:
        logger.error(e)
        exit(1)

def main():
    post = get_post()
    send_twitter_post(post) if TW_POST else None
    send_bluesky_post(post) if BSKY_POST else None

if __name__ == '__main__':
    main()
