import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measure = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    my_date = dt.date(2017, 8, 23)

    # Perform a query to retrieve the data and precipitation scores
    last_year = my_date - dt.timedelta(days=365)

    results = session.query(measure.date, measure.prcp).filter(measure.date >= last_year).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precp
    all_precip = []
    for Date, Precipitation in results:
        precip_dict = {}
        precip_dict["date"] = Date
        precip_dict["precipitation"] = Precipitation
        all_precip.append(precip_dict)

    return jsonify(all_precip)



@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    
    results = session.query(station.station).all()

    session.close()


    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    my_date = dt.date(2017, 8, 23)

    # Perform a query to retrieve the data and precipitation scores
    last_year = my_date - dt.timedelta(days=365)

    results = session.query(measure.date, measure.prcp).filter(measure.station == 'USC00519281').filter(measure.date >= last_year).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for Date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = Date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)
    
    results = session.query(func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).filter(measure.date >= start).all()

    session.close()


    all_tobs_start = list(np.ravel(results))

    return jsonify(all_tobs_start)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)
    
    results = session.query(func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).\
        filter(measure.date >= start).\
            filter(measure.date <= end).all()

    session.close()


    all_tobs_start = list(np.ravel(results))

    return jsonify(all_tobs_start)

if __name__ == '__main__':
    app.run(debug=True)

