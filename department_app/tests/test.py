"""
Tests to check app
"""
import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + 'api/department/edit/173')
print(response.json())
