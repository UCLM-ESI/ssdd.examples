#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-

from requests import put, get


print(get('http://localhost:5000/').json())

device_id = "door1"
response = get(f'http://localhost:5000/{device_id}')

if response.status_code == 404 or \
   response.json()[device_id] == 'disabled':
    new_status = 'enabled'
else:
    new_status = 'disabled'


put(f'http://localhost:5000/{device_id}', data={'status': new_status})
print(get(f'http://localhost:5000/{device_id}').json())
