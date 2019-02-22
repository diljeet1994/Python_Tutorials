
# coding: utf-8

# ## What is ETL?

# ETL is actually short form of Extract, Transform and Load, a process in which data is acquired, changed/processes and then finally get loaded into data warehouse/database(s).
# 
# You can extract data from data sources like Files, Website or some Database, transform the acquired data and then load the final version into database for business usage.
# 
# You may ask, Why ETL?, well, what ETL does, many of you might already been doing one way or other by writing different functions/scripts to perform tasks but one of the main advantage of ETLs is visualizing your entire data flow pipeline thus help you make decisions according to that.

# Let's start with building our own ETL pipeline. 
# * Extract data from CSV file
# * Transform/Manipulate Data
# * Load Data into MongoDB

# In[ ]:


# to read data from csv, python provides csv module
import csv


# To deal with files in Python, we use the open() function, it’s a built-in Python function. This function accepts two different arguments (inputs) in the parentheses, always in the following order: 
# * the name of the file (as a string) 
# * the mode of working with the file (as a string) 
# 
# The syntax to open a file in python is:
# 
# file_obj = open(“filename”, “mode”)  

# In[ ]:


f = open(r'C:\Users\hp\PycharmProjects\Portfolio_FIL\crypto-markets.csv')
# 'f' is a file handler here

csv_reader = csv.reader(f)
print(csv_reader)


# ![title](Crypto_Market_Data.PNG)

# Transforming/Changing the data.

# In[ ]:


assetsCode = ['BTC', 'ETH', 'XRP', 'LTC']

# initialize empty list
crypto_data = []

next(csv_reader, None)  # skips the headers

# read csv data row wise
for row in csv_reader:
    if(row[1] in assetsCode):  # check if current row consist of either 'BTC' or 'ETH' or 'XRP' or 'LTC' currency data
        # convert open, high, low, close amount to float type first from str and then convert it into GBP 
        row[5] = float(row[5]) * 0.75
        row[6] = float(row[6]) * 0.75
        row[7] = float(row[7])* 0.75
        row[8] = float(row[8]) * 0.75
        crypto_data.append(row)
        
# print(csv_reader.line_num)
print(len(crypto_data))
print(crypto_data[0:2])


# Loading the data into SQL DB 

# In[ ]:


import sqlite3

# connect function opens a connection to the SQLite database file, 
conn = sqlite3.connect('session.db') 
#Similarly we will make connection with other databases like Oracle, DB2 etc.


# In[ ]:


# Drop a table name Crypto id it exists already
try:
    conn.execute('DROP TABLE IF EXISTS `Crypto` ')
except Exception as e:
    print(str(e))


# In[ ]:


# Create a new Table named as Crypto
try:
    conn.execute('''
         CREATE TABLE Crypto
         (ID         INTEGER PRIMARY KEY,
         NAME        TEXT    NOT NULL,
         Date        datetime,
         Open        Float DEFAULT 0,
         High        Float DEFAULT 0,
         Low         Float DEFAULT 0,
         Close       Float DEFAULT 0);''')
    print ("Table created successfully");
except Exception as e:
    print(str(e))
    print('Table Creation Failed!!!!!')
finally:
    conn.close() # this closes the database connection


# In[ ]:


# Since our crypto data contains more information than required so we need eliminate some of it.
print(crypto_data[0])


# In[ ]:


# Some more transformations
crypto_sql_data = [(row[2], row[3], row[5], row[6], row[7], row[8]) for row in crypto_data]
crypto_sql_data[:2]


# In[ ]:


# lets make new connection to Insert crypto data in SQL DB
conn = sqlite3.connect('session.db')
cur = conn.cursor()
try:
    cur.executemany("INSERT INTO Crypto(NAME, Date, Open, High, Low, Close) VALUES (?,?,?,?,?,?)", crypto_sql_data)
    conn.commit()
    print('Data Inserted Successfully')
except Exception as e:
    print(str(e))
    print('Data Insertion Failed')
finally:
    conn.close()


# In[ ]:


# Let's Read data from DB to verify it

conn = sqlite3.connect('session.db')
rows = conn.cursor().execute('Select * from Crypto')

for row in rows:
    print(row)


# Write data in a csv file

# In[ ]:


csvfile = open('Crypto.csv', 'w') 
csv_writer = csv.writer(csvfile, lineterminator='\r')
# Now we can write data to files using two methods:
# writerow() or writerows() 
# writerow() is used when we need to write one-dimension data such as a single list :[1, ‘Jerry’, 95] 
# writerows() is used when we need to write multi-dimension data such as list of list [[1, ‘Jerry’, 95], [2, ‘Tom’, 80], [3, ‘Scooby’, 90]]  
# So the only difference is that writerows() lets you pass multiple values! 
csv_writer.writerow(['Name', 'Date', 'Open', 'High', 'Low', 'Close'])
csv_writer.writerows(crypto_sql_data)
csvfile.close()

