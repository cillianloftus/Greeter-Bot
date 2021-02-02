from data.time import current_time, next_tweet_time
from time import sleep, time
from twitter import Twitter

from data.base import Database
from data.redacted import username
from statistics import mean, median

def greet():
  # user = Twitter.User(username)
  user = Twitter.User.random()
  # print(user.username)
  user.greet()
  # user.log()

def main():
  # Database.reset()
  # Twitter.delete_tweets()
  # Twitter.update_description()
  
  # greet()
  test()

def test():
  i = 0
  run_times = []
  while i < 144:
    print()
    i += 1
    print(i)

    while current_time() != next_tweet_time():
      sleep_time = max(0, (next_tweet_time() - current_time()).seconds - 5)
      if sleep_time > 0:
        print(f'Sleep | {sleep_time} seconds')
        sleep(sleep_time)

    print(f'Time | {current_time()}')

    t0 = time()
    user = Twitter.User.random()
    print(f'User | {user.username}')
    user.greet()
    t1 = time()
    delta_t = t1 - t0
    run_times.append(delta_t)
    print(f'Time Taken | {delta_t} seconds')
    Twitter.update_description()
    
  print()
  print(f'Max | {max(run_times)} seconds')
  print(f'Mean | {mean(run_times)} seconds')
  print(f'Median | {median(run_times)} seconds')
  print(f'Min | {min(run_times)} seconds')
  print()

if __name__ == "__main__":
  try:
    main()
  # If any error occurs, update the description to reflect this and then raise the error
  except Exception as exception:
    Twitter.update_description(True)
    raise exception
