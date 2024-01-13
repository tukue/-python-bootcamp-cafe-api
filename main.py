from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask import request
import secrets
from dotenv import load_dotenv

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

load_dotenv()
app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

# api key 
API_KEY= os.getenv("API_KEY")


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Get All Cafes
@app.route("/cafes")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    cafe_list = [cafe.serialize() for cafe in cafes]
    return jsonify(cafes=cafe_list)

@app.route("/cafedataexist")    
def does_cafe_exist():
    cafe = db.session.query(Cafe).all()            
    if cafe!=None:
        return "True"
    else:
        return "False" 

@app.route("/cafes/apikey")
def generatekey():
    api_key= secrets.token_hex(32)
    print(api_key)
    return secrets.token_hex(32)


# HTTP GET - Read Record
@app.route('/cafe/<int:id>', methods=['GET'])
def get_cafe(id):  # Add opening parenthesis after the function name
    cafe = db.session.query(Cafe).get(id)
    if cafe:
        return jsonify(cafe.serialize())
    else:
        return jsonify(error="Cafe not found"), 404 


class Cafe(db.Model):
    # your existing fields here

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'map_url': self.map_url,
            'img_url': self.img_url,
            'location': self.location,
            'seats': self.seats,
            'has_toilet': self.has_toilet,
            'has_wifi': self.has_wifi,
            'has_sockets': self.has_sockets,
            'can_take_calls': self.can_take_calls,
            'coffee_price': self.coffee_price
        }
    
# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add_cafe():
    data=request.get_json()
    
    new_cafe = Cafe(
        name = data.get('name'),
        map_url = data.get('map_url'),
        img_url = data.get('img_url'),
        location = data.get('location'),
        seats = data.get('seats'),
        has_toilet = data.get('has_toilet'),
        has_wifi =  data.get('has_wifi'),
        has_sockets = data.get('has_sockets'),
        can_take_calls = data.get('can_take_calls'),
      coffee_price = data.get('coffee_price')
   )

    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(message="Cafe added successfully")


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_price(cafe_id): 
    data=request.get_json()
    new_price = data.get('new_price')
    if new_price is None:
        return jsonify(error={"Bad request": "No new price provided."}), 400
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(message="Successfully updated the price."), 200
    else:   
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route("/delete/<int:id>", methods=['DELETE'])
def delete_cafe(id):
      
    api_key = request.headers.get('API-Key')
    if api_key !=API_KEY:
        print(api_key)
        print(API_KEY)
        return jsonify(error={"Unauthorized": "Invalid API key"}), 401
    cafe = Cafe.query.get(id)
    if cafe is None:
        return jsonify(error={"Bad request": " a cafe with that ID was not found in the database.."}), 404
    else :
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(message="Cafe deleted successfully"), 200
   
if __name__ == '__main__':
    app.run(debug=True)

 
