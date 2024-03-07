import pandas as pd
from pandas.api.types import is_string_dtype
import requests
import json
import csv

# Function to extract the 'value' from dictionaries
def extract_value(x):
    if isinstance(x, dict) and 'value' in x:
        return x['value']
    return x  # Return as is if not a dictionary or 'value' key is missing


contact_list = []
max_results = 20
count = 20
headers = {'Authorization': 'Bearer %s' % 'pat-na1-2a7386fc-688b-4427-b05e-bed4e1fb01c7'}
url = 'https://api.hubapi.com/contacts/v1/lists/all/contacts/all'
params = {'property': ['investor_id' ,'email', 'firstname', 'lastname', 'hubspotscore', 'hs_analytics_num_visits' ,'hs_analytics_num_page_views','hs_analytics_last_visit_timestamp', 'hs_email_open', 'hs_email_last_open_date','hs_email_last_click_date'], 'propertyMode': 'value_only', 'count': count}


has_more = True
while has_more:
   response = requests.get(url, headers = headers, params=params)
   data = response.json()
   dp = data['contacts'][0]
   # for contact in data['contacts']:
   #    print(contact['properties']['hs_analytics_num_page_views']['value'])
   has_more = data['has-more']
   contact_list.extend(data['contacts'])
   params['vidOffset'] = data['vid-offset']
   if len(contact_list) >= max_results: # Exit pagination, based on whatever value you've set your max results variable to.
      print('maximum number of results exceeded')
      break

df1 = pd.DataFrame(contact_list)
df2 = pd.DataFrame([item['properties'] for item in contact_list])
# Apply the function to each element in the DataFrame
df2 = df2.applymap(extract_value)
df3 = pd.concat([df1.reset_index(drop=True),df2.reset_index(drop=True)], axis=1)
#df4 = df3.iloc[:,13:15]
cols = ['investor_id' ,'email', 'firstname', 'lastname', 'hubspotscore', 'hs_analytics_num_visits' ,'hs_analytics_num_page_views','hs_analytics_last_visit_timestamp', 'hs_email_open', 'hs_email_last_open_date','hs_email_last_click_date']
df5=df3[cols]
#datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
# for col in df3:
#    if isinstance(df3[col], dict):
#       print(df3[col])
#       df3[col] = df3[col]['value']
#          # str.replace('{\'value\': \'','')

df5.to_csv('contacts.csv', sep=',')