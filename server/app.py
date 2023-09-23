#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def bakery_by_id(id):

    # step 1: find bakery using id
    bakery = Bakery.query.filter_by(id=id).first()

    # step 2: Define General if not found REsponse
    if not bakery:
        response = make_response(
            'bakery not found',
            400
        )

        return response

    # handling GET Requests
    if request.method == 'GET':
        bakery_serialized = bakery.to_dict()

        response = make_response(
            bakery_serialized,
            200
        )
        return response
    
    # handling PATCH Requests
    elif request.method == 'PATCH':

        # step 1: iterate through form,  for every key in form, 
            # find corresponding key in review and set it to value of key in form
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

        # step 2: add UPDATED instance to to session and commit to session
        db.session.add(bakery)
        db.session.commit()

        # step 3: convert UPDATED instance to dictionary and return it alongside status code
        bakery_dict = bakery.to_dict()

        response = make_response(
            bakery_dict,
            200
        )

        return response




@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response


@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():

    # handling GET Request
    if request.method == 'GET':
        baked_goods = BakedGood.query.all()

        baked_goods_array = []

        for baked_good in baked_goods:

            baked_goods_dict = {
                'id': baked_good.id,
                'name': baked_good.name,
                'price': baked_good.price,
                'created_at': baked_good.created_at
            }
            baked_goods_array.append(baked_goods_dict)
        
        response = make_response(
            jsonify(baked_goods_array),
            200
        )
        return response

    # handling POST Request
    elif request.method == 'POST':

        # step 1: extract values from form to create new Review Instance
        new_baked_good = BakedGood(
            name = request.form.get('name'),
            price = request.form.get('price'),
            bakery_id = request.form.get('bakery_id')

        )

        # step 2: add new instance to to session and commit to session
        db.session.add(new_baked_good)
        db.session.commit()

        # step 3: convert new instance to dictionary and return it alongside status code
        new_baked_good_dict = new_baked_good.to_dict()

        response = make_response(
            new_baked_good_dict,
            201
        )

        return response


@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def baked_good_by_id(id):

    # step 1 find baked_good using id
    baked_good =  BakedGood.query.filter(BakedGood.id == id).first()

     # step 2: Define General if not found REsponse
    if not baked_good:
        response = make_response(
            'baked_good not found',
            400
        )

        return response
    
    # step 3: handle GET Request
    if request.method == 'DELETE':
        db.session.delete(baked_good)
        db.session.commit()

        response_body = {
            'delete successful': True,
            'message': 'Review successfully deleted'
        }

        response = make_response(
            response_body,
            200
        )

        return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
