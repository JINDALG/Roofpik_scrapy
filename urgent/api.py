from flask_restful import Resource
from flask_restful import Api
from flask_cors import CORS
from flask import Flask, jsonify
from flask import request
from flask_restful import reqparse
from datetime import timedelta
from flask import make_response, current_app
from functools import update_wrapper
import subprocess
import os

from pprint import pprint
import json
import traceback


app = Flask(__name__)
api = Api(app)
CORS(app)
def entry_data(url):
    try :
        with open('link.txt','w') as f:
            # os.chmod('roofpik/scrapy/project_entry/project_entry/spiders/link.txt', 0777)
            f.write(url)
        if "99acres" in url:
            os.system(os.path.dirname(__file__)+'./acres.sh')
            data = None
            with open('price.json','r') as f:
            # os.chmod('roofpik/scrapy/project_entry/project_entry/spiders/link.txt', 0777)
                data = json.loads(f.read())
                pprint(data)
                for entry in data:
                    try :
                        data[entry]['avg'] = int(data[entry]['avg']/data[entry]['count'])
                    except :
                        pass
            os.remove('price.json')
            return data
        if "common" in url:
            os.system(os.path.dirname(__file__)+'./common.sh')
            data = None
            with open('price.json','r') as f:
            # os.chmod('roofpik/scrapy/project_entry/project_entry/spiders/link.txt', 0777)
                data = json.loads(f.read())
                pprint(data)
                for entry in data:
                    try :
                        data[entry]['avg'] = int(data[entry]['avg']/data[entry]['count'])
                    except :
                        pass

            os.remove('price.json')
            return data
        if "magicbricks" in url:
            os.system(os.path.dirname(__file__)+'./mb_rent.sh')
            data = None
            with open('price.json','r') as f:
            # os.chmod('roofpik/scrapy/project_entry/project_entry/spiders/link.txt', 0777)
                data = json.loads(f.read())
                pprint(data)
                for entry in data:
                    try :
                        data[entry]['avg'] = int(data[entry]['avg']/data[entry]['count'])
                    except :
                        pass

            os.remove('price.json')
            return data
    except Exception,e:
        return str(e)
   
class projectentry(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)
        args = parser.parse_args()
        url = args['url']
        return jsonify(entry_data(url))

api.add_resource(projectentry, '/projectentry')

if __name__ == "__main__":
    # entry_data('http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Gurgaon&projectSocity=vipul%20green')
    app.run(debug = True)