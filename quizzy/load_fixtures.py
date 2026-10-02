#!/usr/bin/env python3
# Loads the sample questions and quizzes of fixtures.json through the API.
# Each run creates new copies, because POST is not idempotent.

import json
import sys
from pathlib import Path

import requests


server = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8000'
fixtures = json.loads(Path(__file__).with_name('fixtures.json').read_text())


def post(path, body):
    "Send a POST request to the API and return the response, or exit on error"
    response = requests.post(server + path, json=body)
    if not response.ok:
        sys.exit(f'POST {path} {response.status_code}: {response.text}')
    return response


# fixtures.json names each question, and the server assigns its id
id_by_name = {name: post('/questions', question).json()['id']
              for name, question in fixtures['questions'].items()}

for quiz in fixtures['quizzes']:
    question_ids = [id_by_name[name] for name in quiz['questions']]
    response = post('/quizzes', {'title': quiz['title'], 'question_ids': question_ids})
    print(f"{quiz['title']:20} {server}/#{response.headers['Location']}")
