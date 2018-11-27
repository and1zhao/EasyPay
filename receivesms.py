from flask import Flask, request, jsonify
from pprint import pprint
import json, os

app = Flask(__name__)


@app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    if request.is_json:
        pprint(request.get_json())
    else:
        data = dict(request.form) or dict(request.args)
        with open('response.json', 'w') as outfile:
            json.dump(data, outfile)
        os.system("python3 execute.py")
        pprint(data)
    return ('', 204)
app.run(port=3000)
