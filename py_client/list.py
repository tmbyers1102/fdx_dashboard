import requests
from getpass import getpass

auth_endpoint = "http://127.0.0.1:8000/api/auth/"
username = input("Enter username\n")
password = getpass("Enter password\n")

auth_response = requests.post(auth_endpoint, json={"username": username, "password": password})
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    endpoint = "http://127.0.0.1:8000/api/products/"

    get_response = requests.get(endpoint, headers=headers)
    
    # want to get the next page of a pagination?
    data = get_response.json()
    next_url = data['next']
    results = data['results']
    print("next url: ", next_url)
    print(results)
    if next_url is not None:
        get_response = requests.get(endpoint, headers=headers)
        print(get_response.json())