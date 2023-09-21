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

@app.route('/baked_goods', methods=['POST'])
# this line of code specilises on the url route and indicates that it should only respond to POST requests
def create_baked_good():
    # Get data from the form
    name = request.form.get('name')
    # it extracts the value of the name field from the data sent in the POST request
    price = float(request.form.get('price'))
    # it extracts the price value from the formdata and converts it into a float

    # Create a new BakedGood instance
    new_baked_good = BakedGood(name=name, price=price)

    try:  
        # we want to capture any potential exception that may occur during interaction
        # Add the new baked good to the database
        db.session.add(new_baked_good)
        db.session.commit()

        # Return the data of the newly created baked good as JSON
        return jsonify({
            'id': new_baked_good.id,
            'name': new_baked_good.name,
            'price': new_baked_good.price
        }), 201  # HTTP status code 201 indicates "Created"
    except Exception as e:
        # Handle any database-related errors
        db.session.rollback()
        return jsonify({'error': 'Failed to create baked good', 'message': str(e)}), 500  # HTTP status code 500 for internal server error


@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    try:
        # inside here we are trying to retrieve a bakery with the specified id
        bakery = Bakery.query.get(id)
        if not bakery:
            return jsonify({'error': 'Bakery not found'}), 404  # HTTP status code 404 for not found
        
        # Get data from the form
        new_name = request.form.get('name')

        # Update the bakery's name if a new name is provided in the form
        if new_name:
            bakery.name = new_name

        # Commit the changes to the database
        db.session.commit()

        # Return the updated bakery data as JSON
        return jsonify(bakery.to_dict()), 200  # HTTP status code 200 for success
    except Exception as e:
        # Handle any database-related errors
        db.session.rollback()
        return jsonify({'error': 'Failed to update bakery', 'message': str(e)}), 500  # HTTP status code 500 for internal server error


@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    # Takes the argument of the id 
    try:
        baked_good = BakedGood.query.get(id)
        # first it retrieves the baked good with the given id
        if not baked_good:
            return jsonify({'error': 'Baked good not found'}), 404  # HTTP status code 404 for not found

        # Delete the baked good from the database
        db.session.delete(baked_good)
        db.session.commit()

        # Return a JSON message confirming the deletion
        return jsonify({'message': 'Baked good deleted successfully'}), 200  # HTTP status code 200 for success
    except Exception as e:
        # if there is any error in the deletion process it catches the execption and rolls back the database transaction using th db.session.rollback()and returns a json response with a 500 status code 
        # Handle any database-related errors
        db.session.rollback()
        return jsonify({'error': 'Failed to delete baked good', 'message': str(e)}), 500  # HTTP status code 500 for internal server error


if __name__ == '__main__':
    app.run(port=5555, debug=True)
