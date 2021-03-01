from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://vgdemwsf:ZiMXizCSA-Rmjq5Wz2xUT0cRin68bpim@ziggy.db.elephantsql.com:5432/vgdemwsf"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Dish(db.Model):
  __tablename__ = 'dishes'

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(), unique=True, nullable=False)
  vegan = db.Column(db.Boolean(), nullable=False)
  cost = db.Column(db.Float(), nullable=False)
  img = db.Column(db.String(), nullable=False)

class DishSchema(ma.SQLAlchemySchema):
  class Meta:
    model = Dish
    fields = ("id", "name", "vegan", "cost", "img")

db.init_app(app) # do i need this?
migrate = Migrate(app, db) # do i need this?

@app.route("/dish")
def get_dishes():
  dishes = Dish.query.all()
  dishes_json = DishSchema(many=True).dump(dishes)
  return jsonify(dishes_json)

@app.route('/dish', methods=["POST"])
def test():
  newDish = Dish(
    name=request.json["name"], 
    vegan=request.json["vegan"], 
    cost=request.json["cost"], 
    img=request.json["img"]
  )
  db.session.add(newDish)
  db.session.commit()
  return DishSchema().dump(newDish)

@app.route("/dish/<int:id>", methods=["PATCH"])
def update_dish(id):
  dish = Dish.query.get(id)
  update = request.json

  if "name" in update:
    dish.name = update["name"]
  if "vegan" in update:
    dish.vegan = update["vegan"]
  if "cost" in update:
    dish.cost = update["cost"]
  if "img" in update:
    dish.img = update["img"]
  db.session.commit()
  return DishSchema().dump(dish)

@app.route("/dish/<int:id>", methods=["DELETE"])
def delete_dish(id):
  dish = Dish.query.get(id)
  db.session.delete(dish)
  db.session.commit()
  return {
    "success": True
  }

if __name__ == '__main__':
    app.run(debug=True)

