#!/usr/bin/env python3
# Uses the Quizzy API with plain HTTP requests: no stubs needed.

import json
import sys

import requests


server = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8000'


def request(method, path, body=None):
    "Send a request to the API, print it with its response, and return the body"
    response = requests.request(method, server + path, json=body)
    print(method, path, response.status_code)
    print(json.dumps(response.json()), end='\n\n')
    return response.json()


tcp_layer = {'text': 'Which layer does TCP belong to?',
             'options': ['network', 'transport', 'application'],
             'correct_option': 1}
ipv4_bits = {'text': 'How many bits does an IPv4 address have?',
             'options': ['32', '48', '64', '128'],
             'correct_option': 0}

question_ids = [request('POST', '/questions', question)['id']
                for question in [tcp_layer, ipv4_bits]]
quiz = request('POST', '/quizzes', {'title': 'Networks', 'question_ids': question_ids})
request('GET', f'/quizzes/{quiz["id"]}')

answers = {question_ids[0]: 1, question_ids[1]: 3}  # the second one is wrong
request('POST', f'/quizzes/{quiz["id"]}/grade', answers)

# invalid: correct_option is not the index of any option
request('POST', '/questions', {'text': 'Wrong', 'options': ['a', 'b'], 'correct_option': 2})
