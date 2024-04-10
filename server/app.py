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


@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return jsonify(bakeries), 200


@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery(id):
    bakery = Bakery.query.get(id)
    if bakery:
        return jsonify(bakery.to_dict()), 200
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.json
    if 'name' in data and 'price' in data and 'bakery_id' in data:
        bakery_id = data['bakery_id']
        bakery = Bakery.query.get(bakery_id)
        if bakery:
            baked_good = BakedGood(name=data['name'], price=data['price'], bakery_id=bakery_id)
            db.session.add(baked_good)
            db.session.commit()
            return jsonify(baked_good.to_dict()), 201
        else:
            return jsonify({'error': 'Bakery not found'}), 404
    else:
        return jsonify({'error': 'Incomplete data provided'}), 400


@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if bakery:
        data = request.json
        if 'name' in data:
            bakery.name = data['name']
            db.session.commit()
            return jsonify(bakery.to_dict()), 200
        else:
            return jsonify({'error': 'No update data provided'}), 400
    else:
        return jsonify({'error': 'Bakery not found'}), 404


@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        return jsonify({'message': 'Baked good deleted successfully'}), 200
    else:
        return jsonify({'error': 'Baked good not found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
