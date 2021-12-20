#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "Pong UCLM", 200


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
