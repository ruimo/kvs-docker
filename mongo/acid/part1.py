import json
from pymongo import MongoClient

class InitData:
  def __init__(self):
    self.client = MongoClient('localhost', 27017)
    self.db = self.client['accounts']
    self.accounts = self.db.accounts
    # drop data from accounts collection every time to start from a clean slate
    self.accounts.drop()
    # load data from json and insert them into our database
    init_data = InitData.load_data(self)
    self.insert_data(init_data)

  @staticmethod
  def load_data(self):
    ret = []
    with open('init_data.json', 'r') as f:
      for line in f:
        ret.append(json.loads(line))
    return ret

  def insert_data(self, data):
    for document in data:
      collection_name = document['collection']
      account_id = document['account_id']
      account_name = document['account_name']
      account_balance = document['account_balance']
      self.db[collection_name].insert_one({'account_id': account_id, 'name': account_name, 'balance': account_balance})

  def transfer(self, source_account, target_account, value):
    print(f'transferring {value} Hypnotons from {source_account} to {target_account}')
    with self.client.start_session() as ses:
      ses.start_transaction()
      self.accounts.update_one({'account_id': source_account}, {'$inc': {'balance': value*(-1)} })
      self.accounts.update_one({'account_id': target_account}, {'$inc': {'balance': value} })
      updated_source_balance = self.accounts.find_one({'account_id': source_account})['balance']
      updated_target_balance = self.accounts.find_one({'account_id': target_account})['balance']
      if updated_source_balance < 0 or updated_target_balance < 0:
        ses.abort_transaction()
      else:
        ses.commit_transaction()

obj = InitData()
obj.transfer('1', '2', 300)

