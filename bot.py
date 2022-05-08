from dateutil import tz
from dateutil.relativedelta import relativedelta
from datetime import datetime

import tweepy
import os
import logging

FORMAT = '[%(levelname)s] [%(asctime)s] %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

MUZSKA_LAST_TWEET_DATE = os.environ.get('MUZSKA_LAST_TWEET_DATE')
MUZSKA_LAST_VIDEO_DATE = os.environ.get('MUZSKA_LAST_VIDEO_DATE')
DATE_FORMAT = os.environ.get('DATE_FORMAT')

CET = tz.gettz('CET')
MUZSKA_LAST_TWEET = datetime.strptime(MUZSKA_LAST_TWEET_DATE, DATE_FORMAT).astimezone(CET)
MUZSKA_LAST_VIDEO = datetime.strptime(MUZSKA_LAST_VIDEO_DATE, DATE_FORMAT).astimezone(CET)

TWEET_MSG = 'Días sin Muzska:\n\nÚltimo tweet: {last_tweet}\nÚltimo video: {last_video}\n\nMuzska te echamos de menos <3'
RELATIVE_MSG = '{num_years} {str_years}, {num_months} {str_months} y {num_days} {str_days}'


def get_relative_time(dt):
    return RELATIVE_MSG.format(num_years=dt.years,
                               str_years='años' if dt.years != 1 else 'año',
                               num_months=dt.months,
                               str_months='meses' if dt.months != 1 else 'mes',
                               num_days=dt.days,
                               str_days='días' if dt.days != 1 else 'día')


def send_tweet_update():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    tw = tweepy.API(auth)

    now = datetime.now().astimezone(CET)
    relative_last_tweet = relativedelta(now, MUZSKA_LAST_TWEET).normalized()
    relative_last_video = relativedelta(now, MUZSKA_LAST_VIDEO).normalized()

    logger.info("Sending Tweet...")
    tw.update_status(TWEET_MSG.format(last_tweet=get_relative_time(relative_last_tweet), last_video=get_relative_time(relative_last_video)))
    logger.info('Tweet sent')


def lambda_handler(event, context):
    try:
        send_tweet_update()
    except Exception as e:
        logger.error(e)
        exit(1)


if __name__ == '__main__':
    send_tweet_update()
