import requests


endpoint = "http://127.0.0.1:8000/api/products/3/"

get_response = requests.get(endpoint)
# , json={"title": "ABC123", "content": "hellow world", "price": "ABC1234"}
print(get_response.json())