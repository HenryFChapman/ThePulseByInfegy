import requests

# Set up authentication parameters
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
authorization_code = 'YOUR_AUTHORIZATION_CODE'
redirect_uri = 'YOUR_REDIRECT_URI'

# Exchange authorization code for access token
token_url = 'https://api.hubapi.com/oauth/v1/token'
token_data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'client_secret': client_secret,
    'code': authorization_code,
    'redirect_uri': redirect_uri
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json()['access_token']

# Set up file upload parameters
file_path = '/path/to/your/file.pdf'
file_name = 'my_file.pdf'
folder_id = 1234567890  # Replace with your actual folder ID

# Upload file to HubSpot
upload_url = 'https://api.hubapi.com/filemanager/api/v3/files'
upload_headers = {
    'Authorization': f'Bearer {access_token}'
}
upload_data = {
    'folder_paths': [f'/folder/{folder_id}'],
    'file_names': [file_name],
    'files': [(file_name, open(file_path, 'rb'), 'application/pdf')]
}
upload_response = requests.post(upload_url, headers=upload_headers, files=upload_data)
file_id = upload_response.json()[0]['id']

print(f'File uploaded with ID {file_id}')
