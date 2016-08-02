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
import scr
def entry_data(url):
    try :
        with open('link.txt','w') as f:
            f.write(url)
        if "99acres" in url:
            scr.acres()
            data = None
            with open('price.json','r') as f:
            # os.chmod('roofpik/scrapy/project_entry/project_entry/spiders/link.txt', 0777)
                data = json.loads(f.read())
                for entry in data:
                    try :
                        data[entry]['avg'] = int(data[entry]['avg']/data[entry]['count'])
                    except :
                        pass
            os.remove('price.json')
            return data
        if "common" in url:
            scr.common()
            data = None
            with open('price.json','r') as f:
            # os.chmod('roofpik/scrapy/project_entry/project_entry/spiders/link.txt', 0777)
                data = json.loads(f.read())
                for entry in data:
                    try :
                        data[entry]['avg'] = int(data[entry]['avg']/data[entry]['count'])
                    except :
                        pass

            os.remove('price.json')
            return data
        if "magicbricks" in url:
            scr.magic()
            data = None
            with open('price.json','r') as f:
                data = json.loads(f.read())
                for entry in data:
                    try :
                        data[entry]['avg'] = int(data[entry]['avg']/data[entry]['count'])
                    except :
                        pass

            os.remove('price.json')
            return data
    except Exception,e:
        return str(e)
   
# class projectentry(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('url', type=str)
#         args = parser.parse_args()
#         url = args['url']
#         return jsonify(entry_data(url))