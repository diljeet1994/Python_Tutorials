
# coding: utf-8

# In[1]:


from pymongo import MongoClient
import pandas as pd

class MongoDB:

    def __init__(self, user, password, host, db_name ,port='27017', authSource='admin'):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.authSource = authSource
        self.uri = 'mongodb://' + self.user + ':' + self.password + '@'+ self.host + ':' + self.port + '/' + self.db_name + '?authSource=' + self.authSource
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print('MongoDB Connection Successful. CHEERS!!!')
        except Exception as e:
            print('Connection Unsuccessful!! ERROR!!')
            print(e)


    def insert_into_db(self, data, collection):
        if isinstance(data, pd.DataFrame):
            try:
                self.db[collection].insert_many(data.to_dict('records'))
                print('Data Inserted Successfully')
            except Exception as e:
                print('OOPS!! Some ERROR Occurred')
                print(e)
            finally:
                self.client.close()
                print('Connection Closed!!!')
        else:
            try:
                self.db[collection].insert_one(data)
                print('Data Inserted Successfully')
            except Exception as e:
                print('OOPS!! Some ERROR Occurred')
                print(e)
            finally:
                self.client.close()
                print('Connection Closed!!!')

