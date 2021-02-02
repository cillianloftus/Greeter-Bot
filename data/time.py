from datetime import datetime, timedelta

def current_time():
  return round_to_second(datetime.today())

# Rounds the current time up to the nearest five minutes
def next_tweet_time():
  return round_to_minute(current_time(), 5)

# Rounds a given time to a given minute
def round_to_minute(time, minute):
  return time + (datetime.min - time) % timedelta(minutes = minute)

# Rounds a given time to the nearest second
def round_to_second(time):
  if time.microsecond >= 500000:
    time += timedelta(seconds = 1)
  return time.replace(microsecond = 0)
