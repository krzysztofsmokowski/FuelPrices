from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from fuelsmod import FuelScrap

app = Flask(__name__)
api = Api(app)

class WrappedFuels(Resource):
    def get(self):
        fs = FuelScrap()
        data = fs.wrapping_prices()
        return data, 200


api.add_resource(WrappedFuels, '/wrapped')
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
