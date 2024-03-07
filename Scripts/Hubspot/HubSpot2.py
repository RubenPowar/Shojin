import requests
import pandas as pd
import json

# Set up the request headers and query parameters
headers = {'Authorization': 'Bearer %s' % 'pat-na1-2a7386fc-688b-4427-b05e-bed4e1fb01c7'}
params = {'property': ['email', 'firstname', 'lastname', 'hs_object_id', 'hs_analytics_num_page_views'], 'propertyMode': 'value_only'}

# Make the initial request to get the first page of contacts
#url = 'https://api.hubapi.com/properties/v1/contacts/groups/named/analyticsinformation'
url = 'https://api.hubapi.com/properties/v1/contacts/groups/named/analyticsinformation?includeProperties=true'

response = requests.get(url, headers=headers)
data = response.json()['properties']
df = pd.DataFrame([item['name'] for item in data], columns=['properties'])
print(df)