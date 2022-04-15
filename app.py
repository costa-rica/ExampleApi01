from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)

#location of database
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
#not necessary but TravisMedia says it will complain in console if we don't do this
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)


#Test route
@app.route('/',methods=['GET'])
def get():
    return jsonify({"key":"value"})


#Product Class/Model <--database
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    
    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#Product Schema
class ProductSchema(ma.Schema):
#This is where you put anythign that you want to show up.
#Anyhting I don't want to show up i don't have to include in Meta
    class Meta:
        fields = ('id','name','description','price','qty')


#Init schema
product_schema = ProductSchema()#strict doesn't seem to work
products_schema = ProductSchema(many=True)#****LEFT off 19:36

#Create a product route
@app.route('/product',methods=['POST'])
def add_product():
    print("add_product accessed")
    
    # print("request object:::", request)
    # formDict = request.form.to_dict()
    # print('formDict::::',formDict)
    # print('request.json[name]::::', request.json['name'])
    # print('request type:::', type(request))
    # print('request dir:::', dir(request))
    print('request type:::', request.data)
    print('request type:::', type(request.data))
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name,description,price,qty)
    
    db.session.add(new_product)
    db.session.commit()
    print("Product sucessfully added")
    return product_schema.jsonify(new_product)


# Get all products
@app.route('/product',methods=['GET'])
def get_products():
    qry = db.session.query(Product).all()
    qry = Product.query.all()
    # print(qry)
    result = products_schema.dump(qry)
    # result = products_schema.dump(all_products)
    print('result:::', type(result), result)
    # return jsonify(result[0].data)
    return jsonify(result)


#Run Server
if __name__ == '__main__':
    app.run(debug=True)







