#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-
# Example based on https://flask-restful.readthedocs.io/en/latest/quickstart.html

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

devices = {}


class Device(Resource):
    def get(self, device_id):
        return {device_id: devices[device_id]}

    def put(self, device_id):
        devices[device_id] = request.form['status']
        return {device_id: devices[device_id]}


api.add_resource(Device, '/<string:device_id>')

if __name__ == '__main__':
    app.run(debug=True)
