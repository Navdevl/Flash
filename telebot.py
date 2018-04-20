#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Navdevl

"""Telegram Bot that could fetch me what I wanted.."""

from telegram.ext import Updater, CommandHandler
import logging
from reddit import Reddit

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
reddit = Reddit()

def start(bot, update):
    update.message.reply_text('Hey Dumbass! Use /set <seconds> to set an interval')

def push(bot, job):
    posts = reddit.get_latest_post()
    for subreddit, post in posts:
        message = "#{0}\n {1} \n {2}".format(subreddit, post.title, post.url)
        bot.send_message(job.context, text=message)

def set_timer(bot, update, args, job_queue, chat_data):
    logger.info("Setting timer")
    try:
        interval = int(args[0])
        if interval < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return
        elif interval < 5:
            update.message.reply_text('Interval should be minimum of 5 minutes. i.e. 300 seconds.')
            return

        job_queue.run_repeating(push, interval=interval, first=0, context=update.message.chat_id)

        update.message.reply_text('Yes, my love ♥️ !')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    updater = Updater(reddit.telegram_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
