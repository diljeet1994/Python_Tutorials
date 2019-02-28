
# coding: utf-8

# In[1]:
from DataSources import Extract
from DataLoad import MongoDB
import urllib
import pandas as pd

class Transformation:
    
    def __init__(self, dataSource, dataSet):
        extractObj = Extract()
        if dataType == 'APIS':
            self.data = extractObj.getAPISData(dataSet)
        elif dataType == 'CSV':
            self.data = extractObj.getCSVData(dataSet)
        else:
            self.data = extractObj.databases(dataSet)
    
    
    def apiEconomy(self):
        gdp_india = {}
        for record in self.data['records']:
            gdp={}
            gdp['GDP_in_rs_cr'] = int(record['gross_domestic_product_in_rs_cr_at_2004_05_prices'])
            gdp_india[record['financial_year']] = gdp
            gdp_india_yrs = list(gdp_india)
        for i in range(len(gdp_india_yrs)):
            if i == 0:
                pass
            else:
                key = 'GDP_Growth_' + gdp_india_yrs[i]
                gdp_india[gdp_india_yrs[i]][key] = round(((gdp_india[gdp_india_yrs[i]]['GDP_in_rs_cr'] -gdp_india[gdp_india_yrs[i-1]]['GDP_in_rs_cr'])/gdp_india[gdp_india_yrs[i-1]]['GDP_in_rs_cr'])*100,2)
        print(gdp_india)
        
        # connection to mongo db
        mongoDB_obj = MongoDB(urllib.parse.quote_plus('root'), urllib.parse.quote_plus('password'), 'host', 'GDP')
        # Insert Data into MongoDB
        mongoDB_obj.insert_into_db(gdp_india, 'India_GDP')
        
        
    def apiPollution(self):
        air_data = self.data['results']
        # Converting nested data into linear structure
        air_list = []
        for data in air_data:
            for measurement in data['measurements']:
                air_dict = {}
                air_dict['location'] = data['location']
                air_dict['city'] = data['city']
                air_dict['country'] = data['country']
                air_dict['parameter'] = measurement['parameter']
                air_dict['value'] = measurement['value']
                air_dict['lastUpdated'] = measurement['lastUpdated']
                air_dict['unit'] = measurement['unit']
                air_dict['sourceName'] = measurement['sourceName']
                air_list.append(air_dict)
        print('len', len(air_list))
        # Convert list of dict into pandas df
        df = pd.DataFrame(air_list, columns=air_dict.keys())
        print(df.size)
        # connection to mongo db
        mongoDB_obj = MongoDB(urllib.quote_plus('root'), urllib.quote_plus('password'), 'host', 'Pollution_Data')
        # Insert Data into MongoDB
        mongoDB_obj.insert_into_db(df, 'Air_Quality_India')

    


# In[8]:


if '__name__' == '__main__':
    dataSource = input("Please Select the DataSource i.e 'API'/'CSV'/'Database': ").lower()
    dataSet = input('Please select the Data set for Transformation: ').title()
    trans_obj = Transformation(dataSource, dataSet)
    funcName = dataSource+dataSet+"()"
    trans_obj.funcName
    
   

