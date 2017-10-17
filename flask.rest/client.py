#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

from requests import put, get

put('http://localhost:5000/device1', data={'status': 'enabled'})
print(get('http://localhost:5000/device1').json())
