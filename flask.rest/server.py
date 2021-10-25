#!/usr/bin/env python3
# -*- coding: utf-8; mode: python -*-

# Example based on https://flask-restful.readthedocs.io/en/latest/quickstart.html

from flask import Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

devices = dict()


class Device(Resource):
    def get(self, device_id):
        if device_id not in devices:
            abort(404)
        return {device_id: devices.get(device_id)}

    def put(self, device_id):
        devices[device_id] = request.form['status']
        return {device_id: devices[device_id]}


api.add_resource(Device, '/<string:device_id>')


if __name__ == '__main__':
    app.run(debug=True)
