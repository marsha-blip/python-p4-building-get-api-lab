#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, abort
from flask_migrate import Migrate
from datetime import datetime
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

def bakery_to_dict(bakery):
    return {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at.isoformat(),
        "baked_goods": [
            {
                "id": bg.id,
                "name": bg.name,
                "price": bg.price,
                "created_at": bg.created_at.isoformat(),
                "bakery_id": bg.bakery_id
            }
            for bg in bakery.baked_goods
        ]
    }

def baked_good_to_dict(bg):
    return {
        "id": bg.id,
        "name": bg.name,
        "price": bg.price,
        "created_at": bg.created_at.isoformat(),
        "bakery_id": bg.bakery_id
    }

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    all_bakeries = Bakery.query.all()
    result = [
        {
            "id": b.id,
            "name": b.name,
            "created_at": b.created_at.isoformat()
        }
        for b in all_bakeries
    ]
    return make_response(jsonify(result), 200)

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        abort(404, description=f"Bakery with id {id} not found")
    return make_response(jsonify(bakery_to_dict(bakery)), 200)

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    result = [ baked_good_to_dict(g) for g in goods ]
    return make_response(jsonify(result), 200)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    bg = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if bg is None:
        abort(404, description="No baked goods found")
    return make_response(jsonify(baked_good_to_dict(bg)), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)


