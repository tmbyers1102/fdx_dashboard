import requests

endpoint = "https://httpbin.org/status/200/"
endpoint = "https://httpbin.org/anything"
endpoint = "http://127.0.0.1:8000/api/"

get_response = requests.post(endpoint, json={"title": "ABC123", "content": "hellow world", "price": "ABC1234"})

print(get_response.json())