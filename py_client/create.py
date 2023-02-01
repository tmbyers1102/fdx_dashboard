import requests


endpoint = "http://127.0.0.1:8000/api/products/"


data = {
    "title": "This is the title field"
}
get_response = requests.post(endpoint, json=data)
# , json={"title": "ABC123", "content": "hellow world", "price": "ABC1234"}
print(get_response.json())