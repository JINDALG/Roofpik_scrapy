from flask import Flask, jsonify
from flask import request
from flask_restful import reqparse
from datetime import timedelta
from flask import make_response, current_app
from functools import update_wrapper
import subprocess
import os
from firebase import firebase
app = Flask(__name__)
from pprint import pprint

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp
            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp
        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def entry_data(url):
    with open('link.txt','w') as f:
        # os.chmod('roofpik/scrapy/project_entry/project_entry/spiders/link.txt', 0777)
        f.write(url)
    if "acres" in url:
        os.system(os.path.dirname(__file__)+'./acres_script.sh')
        fire = firebase.FirebaseApplication('https://abcapp-8345a.firebaseio.com/temp',None)
        data = fire.get('/',None)
        pprint(data)
        return data
    elif "yards" in url:
        os.system(os.path.dirname(__file__)+'./sqyrd_script.sh')
        fire = firebase.FirebaseApplication('https://abcapp-8345a.firebaseio.com/temp',None)
        data = fire.get('/',None)
        pprint(data)
        return data
	# return "somehting"
@app.route('/projectentry/',methods=['POST'])
@crossdomain(origin = '*')
def char_analysis():
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    url = args['url']
    return jsonify(entry_data(url))

@app.route('/testing/',methods=["GET"])
@crossdomain(origin = '*')
def char():
    return jsonify("d,fhs,df")

if __name__ == "__main__":
    # entry_data('http://www.squareyards.com/gurgaon-residential-property/raheja-maheshwara/8462/project')
	app.run(debug = True, host ="192.168.2.39")