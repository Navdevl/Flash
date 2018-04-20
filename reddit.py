import praw
import configparser
import time
from tinydb import TinyDB, Query


CONFIG_FILE = "config.ini"

class Reddit:
  def __init__(self):
    self.db = TinyDB('db.json')
    self.db_query = Query()
    self.get_credentials()
    self.check_credentials()

  def get_credentials(self):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    self.client_id = config['default']['client_id']
    self.client_secret = config['default']['client_secret']
    self.user_agent = config['default']['user_agent']
    self.username = config['default']['username']
    self.password = config['default']['password']
    self.favorite_subreddits = config['default']['favorite_subreddits'].split(',')
    self.telegram_token = config['default']['telegram_token']

  def check_credentials(self):
    self.reddit = praw.Reddit(client_id=self.client_id,
                              client_secret=self.client_secret,
                              user_agent=self.user_agent,
                              username=self.username,
                              password=self.password
                            )

    try:
      print("Welcome, {0} ".format(self.reddit.user.me()))
    except:
      print("Please check your credentials.")
      exit(0)

  def insert_to_db(self, subreddit, submission):
    subreddit = self.reddit.subreddit(subreddit)
    self.db.insert({'subreddit': subreddit.display_name, 'id': submission.id})

  def get_latest_post(self):
    print("Getting latest posts")
    posts = []
    for subreddit in self.favorite_subreddits:
      for submission in self.reddit.subreddit(subreddit).hot(limit=5):
        submission_results = self.db.search((self.db_query.id == submission.id) & (self.db_query.subreddit == subreddit))
        if submission_results:
          self.insert_to_db(subreddit, submission)
          posts.append([subreddit, submission])
      time.sleep(1)

    return posts
