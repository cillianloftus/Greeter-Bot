from data.file import load_json, write_json

class Database:
  @classmethod
  def entry(cls, user_id):
    return cls.load()[user_id]

  @classmethod
  def includes(cls, user_id):
    return user_id in list(cls.load().keys())

  @classmethod
  def insert(cls, user_id):
    users = cls.load()
    users[user_id] = 0
    cls.save(users)

  @classmethod
  def reset(cls):
    cls.save({})

  @classmethod
  def update(cls, user_id):
    if not(cls.includes(user_id)):
      cls.insert(user_id)

    users = cls.load()
    users[user_id] += 1

    cls.save(users)

  @classmethod
  def users_greeted_data(cls):
    data = {}
    users = cls.load()

    values = list(users.values())
    keys = list(set(values))
    keys.sort()

    for key in keys:
      data[key] = values.count(key)
    
    return data
  
  @staticmethod
  def load():
    return load_json('users')

  @staticmethod
  def save(data):
    write_json(data, 'users')
