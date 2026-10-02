Quizzy, a REST API for multiple-choice quizzes: create questions and quizzes, and answer
a quiz to get a grade (grades are not stored). Built with FastAPI, which
validates requests with Pydantic and stores data in SQLite through the
SQLAlchemy ORM. The client uses plain HTTP (`requests`), no stubs needed.

| Method | Path                       | Effect                                 |
|--------|----------------------------|----------------------------------------|
| POST   | /questions                 | create a question                      |
| GET    | /questions                 | list the questions, with their answers |
| GET    | /questions/{question_id}   | get a question, with its answer        |
| PUT    | /questions/{question_id}   | replace a question                     |
| POST   | /quizzes                   | create a quiz from existing questions  |
| GET    | /quizzes                   | list the quizzes                       |
| GET    | /quizzes/{quiz_id}         | get a quiz, without the answers        |
| PUT    | /quizzes/{quiz_id}         | replace the title and questions        |
| POST   | /quizzes/{quiz_id}/grade   | grade the answers                      |


Depends
-------

Debian packages:

- python3-fastapi
- python3-uvicorn
- python3-sqlalchemy
- python3-requests

or with uv (pip / pipx):

    $ uv sync


Run server
----------

    $ ./server.py

(or `uv run ./server.py`). Data is stored in `quizzy.db`; remove it to start
over. The API description (OpenAPI) is at http://127.0.0.1:8000/openapi.json
and interactive docs at http://127.0.0.1:8000/docs


Run client
----------

    $ ./client.py


Sample data
-----------

    $ ./load_fixtures.py

loads the questions and quizzes in `fixtures.json` through the API. Each run
creates new copies, because POST is not idempotent.

Web client
----------

With the server running, open http://127.0.0.1:8000/ in a browser. It is a
single page (`index.html`) with plain JavaScript: no frameworks, no npm, no
build step. The server itself serves it, so the page and the API share the
same origin and no CORS configuration is needed.


Run with curl
-------------

    $ curl -i -H 'Content-Type: application/json' \
        -d '{"text": "Which layer does TCP belong to?", "options": ["network", "transport", "application"], "correct_option": 1}' \
        http://127.0.0.1:8000/questions
    $ curl -i -H 'Content-Type: application/json' \
        -d '{"title": "Networks", "question_ids": [1]}' http://127.0.0.1:8000/quizzes
    $ curl http://127.0.0.1:8000/quizzes/1
    $ curl -H 'Content-Type: application/json' -d '{"1": 1}' \
        http://127.0.0.1:8000/quizzes/1/grade


Demo
----

    $ ./demo.sh    # requires tmux
