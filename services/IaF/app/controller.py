from flask import jsonify, request

from app import app
from app.models import *
from app.database import engine


def seid(sid, eid):
    eid = eid if len(eid) == 2 else '0' + eid
    sid = sid if len(sid) == 2 else '0' + sid
    return sid + eid


@app.route('/characters', methods=['POST'])
def get_characters():
    slugs = request.get_json()
    results = Character.query.filter(Character.slug.in_(slugs)).all()
    characters = []
    for result in results:
        c = dict(result.__dict__)
        c.pop('_sa_instance_state')
        characters.append(c)
    return jsonify(characters), 200

@app.route('/character/<slug>', methods=['GET'])
def character(slug):
    c = Character.query.filter(Character.slug == slug)[0]
    if c:
        c = dict(c.__dict__)
        c.pop('_sa_instance_state')
        return jsonify(c), 200
    return "Character Not Found", 404


@app.route('/house/<slug>', methods=['GET'])
def house(slug):

    c = House.query.filter(House.slug == slug)[0]
    if c:
        c = dict(c.__dict__)
        c.pop('_sa_instance_state')
        return jsonify(c), 200
    return "House Not Found", 404


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = "Content-Type, x-access-token, Accept"
    header['Access-Control-Allow-Methods'] = "GET, POST, DELETE"
    return response
