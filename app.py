import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return(
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&ltstart&gt<br>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.asc()).all()
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def temps():
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-18').all()
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    temps = []
    results = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date > start).all()
    for date, minim, maxim, avger in results:
        temp = {}
        temp['date'] = date
        temp["min"] = minim
        temp['max'] = maxim
        temp['avg'] = avger
        temps.append(temp)
    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):
    temps = []
    results = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date.between(start, end)).all()
    for date, minim, maxim, avger in results:
        temp = {}
        temp['date'] = date
        temp["min"] = minim
        temp['max'] = maxim
        temp['avg'] = avger
        temps.append(temp)
    return jsonify(temp)

if __name__ == '__main__':
    app.run(debug=True)