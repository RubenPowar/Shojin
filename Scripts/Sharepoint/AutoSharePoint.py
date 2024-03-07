import requests
import json

# Microsoft Graph API endpoint for SharePoint (using the Site ID)
site_id = "site_id"
graph_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/"

# Your Azure AD app registration details
client_id = "your-client-id"
client_secret = "your-client-secret"
tenant_id = "your-tenant-id"

# Get an access token using client credentials flow
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_data = {
    "grant_type": "client_credentials",
    "scope": "https://graph.microsoft.com/.default",
    "client_id": client_id,
    "client_secret": client_secret,
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json().get("access_token")

# Create a folder named "New Folder" in the Shared Documents library
folder_name = "New Folder"
folder_data = {
    "name": folder_name,
    "folder": {},
    "@microsoft.graph.conflictBehavior": "rename",
}

create_folder_url = f"{graph_url}/{folder_name}"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

create_folder_response = requests.put(create_folder_url, headers=headers, data=json.dumps(folder_data))

if create_folder_response.status_code == 201:
    print(f"Folder '{folder_name}' created successfully.")
else:
    print(f"Failed to create folder. Status code: {create_folder_response.status_code}")
    print("Response content:")
    print(create_folder_response.text)


# Sources:
#     https://medium.com/@jorgerocha_85306/automating-sharepoint-management-with-python-creating-folders-made-easy-501c39b4d7e3