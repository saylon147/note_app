# import secrets
#
# secret_key = secrets.token_hex(32)
# print(secret_key)


import requests

api_url = "http://localhost:5000/auth/usernames"
response = requests.get(api_url)
print(response.text)
