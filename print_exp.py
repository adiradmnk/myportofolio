import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portofolio.settings')
django.setup()

from django.test import Client
c = Client()
response = c.get('/experience/')
print(response.content.decode('utf-8'))
