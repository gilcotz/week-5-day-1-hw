from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import db, User, Car, car_schema, cars_schema


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}

# create car
@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    car_model = request.json['car_model']
    car_year = request.json['car_year']
    car_brand = request.json['car_brand']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')
    
    car = Car(name, description, price, car_model, car_year, car_brand, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# retrieve all cars
@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token=owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

#retrieve a single car
@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_car(current_user_id, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)


#update a car by ID
@api.route('/cars/<id>', methods=['POST'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    print(car)
    if car:  
        car.name = request.json['name']
        car.description = request.json['description']
        car.price = request.json['price']
        car.car_model = request.json['car_model']
        car.car_year = request.json['car_year']
        car.car_brand = request.json['car_brand']
        car.user_token = current_user_token.token
        db.session.commit()
        
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error': 'that car does not exist'})

    response = car_schema.dump(car)
    return jsonify(response)


# delete car by ID
@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()

        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error': 'that car does not exist anymore'})