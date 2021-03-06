import pymongo

class MongoController():
  __client = None
  __db = None
  __co = None
  
  def __init__(self, host, port):
    self.__client = pymongo.MongoClient(str(host), int(port))
    self.__db = self.__client.resetter

  def __del__(self):
    self.close()

  def select_coll_tokens(self):
    self.__co = self.__db.tokens
  
  def add_token(self, uid, token):
    self.select_coll_tokens()
    return self.__co.update_one({"uid": uid}, {"$set": {"token": token}})

  def get_token(self, uid):
    self.select_coll_tokens()
    return self.__co.find_one({"uid": uid})

  def close(self):
    self.__client.close()
