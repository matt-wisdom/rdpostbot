import logging
import os
import argparse
import time
import praw

import json
import config
from .preprocess import process
from .model import Messages, Message

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename="bot.log",
    filemode="w",
)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger().addHandler(console)

logger.setLevel(logging.DEBUG)

reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    username=config.user,
    password=config.password,
    redirect_uri=config.redirect_uri,
    user_agent=config.user_agent,
)


def send_to_sub(subreddit: praw.reddit.Subreddit, message: Message):
    flair = message.flair
    flair_id = ""
    if flair:
        for sub_flair in list(subreddit.flair.link_templates.user_selectable()):
            if sub_flair["flair_text"] == flair:
                flair_id = sub_flair["flair_template_id"]
                logger.info(f"Flair_ID:{flair_id}")
    images = message.images
    if images:
        logging.info(f"Sending gallery: {images}")
        for image in images:
            if not os.path.exists(image):
                raise FileNotFoundError(f"{image} not found")
        post = subreddit.submit_gallery(
            title=message.title,
            images=[{"image_path": image} for image in message.images],
        )
    else:
        logger.info(f"Sending '{message.title[:10]}...' to {subreddit}")
        post = subreddit.submit(title=message.title, selftext=message.body, flair_id=flair_id)
    logger.info(f"Sent")
    if message.comment:
        logger.info(f"Commenting {message.comment}")
        post.reply(message.comment)
        


def send_messages():
    messages = Messages.parse_obj(json.load(open("messages.json"))).messages
    for message in messages:
        for subreddit in message.subreddits:
            message.title = process(message.title)
            message.body = process(message.body)
            subreddit = reddit.subreddit(subreddit)
            send_to_sub(subreddit, message)
            time.sleep(message.interval)

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--wait", type=int, help="Wait x seconds before starting")

def main():
    logger.info("Starting")
    args = parser.parse_args()
    if args.wait:
        logger.info(f"Waiting for {args.wait} seconds")
        time.sleep(args.wait)
    for round in range(config.rounds):
        logger.info(f"Starting round {round}")
        send_messages()
        logger.info(f"Round {round} finished")
        time.sleep(config.round_interval)
    logger.info("Done")


if __name__ == "__main__":
    main()
