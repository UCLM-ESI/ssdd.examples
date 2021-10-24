#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-

from requests import put, get


device_id = "device1"
device_response = get(f'http://localhost:5000/{device_id}')

if device_response.status_code == 404 or device_response.json()[device_id] == 'disabled':
    new_status = 'enabled'

else:
    new_status = 'disabled'


put(f'http://localhost:5000/{device_id}', data={'status': new_status})
print(get(f'http://localhost:5000/{device_id}').json())
