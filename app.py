from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://anqlvama:NJcfHCsk6OYBFVeDpnJb0MovkI8RcAWi@ziggy.db.elephantsql.com:5432/anqlvama"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Tank(db.Model):
  __tablename__ = 'tempTank'

  id = db.Column(db.Integer, primary_key = True)
  location = db.Column(db.String(), unique=True, nullable=False)
  lat = db.Column(db.String(), nullable=False)
  long = db.Column(db.String(), nullable=False)
  percentage_full = db.Column(db.Integer(), nullable=False)

class TankSchema(ma.SQLAlchemySchema):
  class Meta:
    model = Tank
    fields = ("id", "location", "lat", "long", "percentage_full")

db.init_app(app) # do i need this?
migrate = Migrate(app, db) # do i need this?

@app.route("/tank")
def get_tempTank():
  tempTank = Tank.query.all()
  tempTank_json = TankSchema(many=True).dump(tempTank)
  return jsonify(tempTank_json)

@app.route('/tank', methods=["POST"])
def test():
  newTank = Tank(
    location=request.json["location"], 
    lat=request.json["lat"], 
    long=request.json["long"], 
    percentage_full=request.json["percentage_full"]
  )
  db.session.add(newTank)
  db.session.commit()
  return TankSchema().dump(newTank)

@app.route("/tank/<int:id>", methods=["PATCH"])
def update_tank(id):
  tank = Tank.query.get(id)
  update = request.json

  if "location" in update:
    tank.location = update["location"]
  if "lat" in update:
    tank.lat = update["lat"]
  if "long" in update:
    tank.long = update["long"]
  if "percentage_full" in update:
    tank.percentage_full = update["percentage_full"]
  db.session.commit()
  return TankSchema().dump(tank)

@app.route("/tank/<int:id>", methods=["DELETE"])
def delete_tank(id):
  tank = Tank.query.get(id)
  db.session.delete(tank)
  db.session.commit()
  return {
    "success": True
  }

if __name__ == '__main__':
    app.run(debug=True)

