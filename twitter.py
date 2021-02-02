from data.base import Database
from data.main import generate_greeting, get_random_term
from data.redacted import api_key, api_secret, access_token, access_secret, backup_description
from data.string import convert_num_to_multiplicative, format_key, pluralise
from datetime import date
import random
import tweepy

class Twitter:
  class Tweet:
    @classmethod
    def sample(cls):
      term = get_random_term()
      tweets = []

      # Save tweets associated with the term to an array
      try:
        for tweet in tweepy.Cursor(Twitter.api.search, q = term, count = Twitter.max_search_results, lang = 'en', result_type = 'mixed').items():
          tweets.append(tweet)
          # If enough tweets have been saved to the array, break the loop
          if len(tweets) == Twitter.max_search_results:
            break
      # If there's a max retries exceeded error, try it again with a new term
      except tweepy.error.TweepError:
        return []

      # If there are no tweets relating to the term, recall the function
      # Otherwise, shuffle and return the array
      if len(tweets) == 0:
        return cls.sample()
      else:
        random.shuffle(tweets)
        return tweets

  class User:
    def __init__(self, data):
      # If an ID/username has been passed instead of an object,
      # find the data associated with the given ID
      if type(data) == str:
        data = Twitter.User.find(data)
      
      self.id = str(data.id)
      self.name = data.name
      # self.username = f'@{data.screen_name}'
      self.username = data.screen_name

      self.cake_day = data.created_at.date()
      # self.cake_day = date.today()

      self.follower_count = data.followers_count
      self.following_count = data.friends_count
      self.tweet_count = data.statuses_count

      self.following = data.following
      self.has_default_profile_img = data.default_profile_image
      self.is_private = data.protected
      self.is_verified = data.verified
      # self.is_verified = True

    def follow(self):
      print(f'Following {self.username}')
      # self.api.follow()

    def greet(self, error = False):
      # If the user is not in the database, insert them
      if not(Database.includes(self.id)):
        Database.insert(self.id)
      
      # If an error has not occurred, update the user in the database
      if not(error):
        Database.update(self.id)

      # Follow the user if they are worthy
      if self.is_chad and not(self.following):
        self.follow()

      try:
        # In the event of an error, call the generate_greeting function with an error flag
        if error:
          Twitter.tweet(generate_greeting(self, Twitter.max_tweet_length, True))
        else:
          Twitter.tweet(generate_greeting(self, Twitter.max_tweet_length))
      # If we're trying to tweet something we've already tweeted before,
      # recall the greeting with an error flag 
      except tweepy.error.TweepError:
        self.greet(True)

    def log(self):
      keys = list(vars(self).keys())
      values = list(vars(self).values())
      for i in zip(keys, values):
        print(f'{format_key(keys[i])} | {values[i]}')

    @classmethod
    def find(cls, id):
      return Twitter.api.get_user(id)

    @classmethod
    def random(cls):
      # Get a random sample of tweets
      tweets = Twitter.Tweet.sample()

      # Loop through the tweets and instantiate a user for the author of each
      # If this user is a suitable candidate, return them
      for tweet in tweets:
        user = cls(tweet.author)
        if user.is_suitable:
          return user

      # If none of the users are deemed suitable, recall the function
      return cls.random()

    # Return the user as an User object from the api
    @property
    def api(self):
      return self.find(self.id)

    @property
    def db_entry(self):
      return Database.entry(self.id)

    @property
    def has_clout(self):
      return (self.follower_count >= Twitter.min_follower_count) and (self.following_count < self.follower_count * 1.5) and (self.tweet_count >= Twitter.min_tweet_count)

    @property
    def has_public_account(self):
      return not(self.has_default_profile_img) and not(self.is_private)

    # Check if today is the users cake day
    @property
    def is_cake_day(self):
      today = date.today()
      return today.day == self.cake_day.day and today.month == self.cake_day.month

    @property
    def is_chad(self):
      return self.num_of_times_greeted > 1

    @property
    def is_suitable(self):
      return self.has_clout and self.has_public_account

    @property
    def num_of_times_greeted(self):
      return self.db_entry if Database.includes(self.id) else 0

  # Setting up the API
  auth = tweepy.OAuthHandler(api_key, api_secret)
  auth.set_access_token(access_token, access_secret)
  api = tweepy.API(auth, compression = True, retry_count = 3, retry_delay = 5, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

  # Setting the constants
  max_days_since_last_tweet = 3
  max_description_length = 160
  max_search_results = 100
  max_tweet_length = 280
  min_follower_count = 100
  min_following_count = min_follower_count
  min_tweet_count = min_follower_count * 5

  @classmethod
  def delete_tweets(cls):
    for status in tweepy.Cursor(cls.api.user_timeline).items():
      cls.api.destroy_status(status.id)

  @classmethod
  def tweet(cls, text):
    cls.api.update_status(text, trim_user = True)
    print(text)

  @classmethod
  def update_description(cls, error = False):
    # If an error description is specified, use that one
    if error:
      description = backup_description
    else:
      data = Database.users_greeted_data()
      sections = []

      keys = list(data.keys())
      values = list(data.values())
      first_loop = True
      for key, value in zip(keys, values):
        text = f'{value:,}'

        # Ensure that the term 'greeted' is only present in the first part
        # (it should be obvious for the rest)
        if first_loop:
          term = 'user' if value == 1 else pluralise('user')
          text += f' {term} greeted'
          first_loop = False

        # Only specifies the number of times greeted if there's more than one key
        if len(keys) > 1:
          text += f' {convert_num_to_multiplicative(key)}'
        
        sections.append(text)

      description = ',\n'.join(sections)
      # If the description is too long or an error description is needed
      if len(description) > Twitter.max_description_length:
        description = backup_description

    cls.update_profile(description = description)

  @classmethod
  def update_profile(cls, description = None, location = None, name = None, url = None):
    try:
      cls.api.update_profile(name, url, location, description)
    except tweepy.error.TweepError:
      return