""" 
    Runs the server and parsers API requests 
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api, Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy import and_

from models import Device
from database import db_session

app = Flask(__name__)
api = Api(app)

class DeviceResource(Resource):
    """
        The device resources handles API requests relating to robomussel data
        it additionally supports facilities to filter datasets based on query
        string parameters
    """
    def get(self, dev_name):
        return map(Device.to_json, 
                self.filter(Device.query.filter(Device.name == dev_name)).all())

    def filter(self, devs):
        args = self.query_parse()
        if args["start_date"] and args["end_date"]:
            devs = devs.filter(Device.date.between(args["start_date"], 
                                                   args["end_date"]))
        return devs

    def query_parse(self):
        parser = RequestParser()
        parser.add_argument('start_date', type=str, location='args')
        parser.add_argument('end_date', type=str, location='args')
        return parser.parse_args()

api.add_resource(DeviceResource, "/api/dev/<string:dev_name>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
