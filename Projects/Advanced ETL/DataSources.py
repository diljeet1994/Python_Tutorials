import csv
import requests
import json

class Extract:
    
    def __init__(self):
        self.data_sources = json.load(open('data_config.json'))
        self.api = self.data_sources['data_sources']['api']
        self.csv_path = self.data_sources['data_sources']['csv']
    
    
    def getAPISData(self, api_name):
        api_url = self.api[api_name]
        response = requests.get(api_url)
        return response.json()

    
    def getCSVData(self, csv_name):
        csv_data = []
        csv_reader = csv.reader(open(self.csv_path[csv_name], 'r'))
        for row in csv_reader:
            csv_data.append(row)
        return csv_data
    
    
    def databases(self, db_name):
        pass
        