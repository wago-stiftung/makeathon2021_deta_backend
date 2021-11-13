from deta import Deta
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
load_dotenv()

DETA_KEY = os.environ.get('DETA_KEY', None)

if DETA_KEY:
    deta = Deta(DETA_KEY)
else:
    deta = Deta()

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_root():
    return 'WAGO Stiftung - Makeathon 2021 - Workshop Deta Cloud'

#########################################################
## LIGHTS - READ
#########################################################

LIGHTNAMES = [
    'bad1',
    'bad2',
    'bad3',
    'couchtisch',
    'esstisch',
    'flur',
    'gaestezimmer',
    'garderobe',
    'kueche',
    'schlafzimmer',
    ]

db_lights = deta.Base('lights')
# Diese Zeile nur beim ersten Aufruf, danach neu Deploy, da hiermit nur per Computer ein paar Daten angelegt werden.
# db_lights.put_many([dict(key=n, value=False) for n in LIGHTNAMES])

@app.route('/lights', methods=['GET'])
def get_lights():
    lightlist = db_lights.fetch()
    result = list(
        map(
            lambda d: (d['key'], d['value']),
            lightlist.items
        )
    )
    return jsonify(dict(result))

@app.route('/lights/<name>', methods=['GET'])
def get_light(name):
    light = db_lights.get(name)
    return jsonify(light['value']) if light else jsonify({"error": "Not found"}, 404)

#########################################################
## LIGHTS - WRITE
#########################################################

@app.route('/lights/<name>', methods=['POST'])
def set_light(name):
    value = request.json
    if type(value) == bool:
        if db_lights.get(name):
            db_lights.put(value, name)
            return jsonify(value, 201)
    return jsonify({"error": "Not found"}, 404)
