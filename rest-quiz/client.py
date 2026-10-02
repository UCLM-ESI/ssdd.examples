#!/usr/bin/env python3

import json
import sys

import requests


url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8000'


def show(response):
    print(response.request.method, response.request.path_url,
          response.status_code)
    print(json.dumps(response.json()), end='\n\n')
    return response.json()


questions = [
    {'text': 'Which layer does TCP belong to?',
     'options': ['network', 'transport', 'application'], 'correct': 1},
    {'text': 'How many bits does an IPv4 address have?',
     'options': ['32', '48', '64', '128'], 'correct': 0},
]

ids = [show(requests.post(f'{url}/questions', json=q))['id']
       for q in questions]

quiz = show(requests.post(f'{url}/quizzes',
                          json={'title': 'Networks', 'questions': ids}))
show(requests.get(f'{url}/quizzes/{quiz["id"]}'))

answers = {ids[0]: 1, ids[1]: 3}
show(requests.post(f'{url}/quizzes/{quiz["id"]}/grade', json=answers))

# 'correct' is not the index of any option
show(requests.post(f'{url}/questions',
                   json={'text': 'Wrong', 'options': ['a', 'b'], 'correct': 2}))
