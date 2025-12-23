# WithoutMuzska Bot

This is a small script that handles the bot on Twitter and Bluesky. The bot code runs with an AWS lambda function.

Twitter: [@WithoutMuzska](https://twitter.com/WithoutMuzska)
Bluesky [@withoutmuzska.bsky.social](https://bsky.app/profile/withoutmuzska.bsky.social)

## Enviroment Variables

| Name | Description |
| ----------- | ----------- |
| TW_CONSUMER_KEY | Consumer key required by Twitter API |
| TW_CONSUMER_SECRET | Consumer secret key required by Twitter API |
| TW_ACCESS_KEY | Access key required by Twitter API |
| TW_ACCESS_SECRET | Access secret key required by Twitter API |
| BSKY_USERNAME | Username of Bluesky account |
| BSKY_APP_PASSWORD | App Password generated in Bluesky account |
| MUZSKA_LAST_VIDEO_DATE | Date of the last video of Muzska |
| DATE_FORMAT | Format used to indicate the dates of last video and last tweet |
| TW_POST | Variable to enable Twitter post |
| BSKY_POST | Variable to enable Bluesky post |
