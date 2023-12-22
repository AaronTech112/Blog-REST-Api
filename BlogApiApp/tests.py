from django.test import TestCase
import requests
# Create your tests here.

request = requests.get('http://127.0.0.1:8000/get_all_posts')

print(request.json())

