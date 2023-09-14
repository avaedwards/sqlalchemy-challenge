# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
def welcome():
    #List all available api routes.
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

    # Query last year of dates and precipitation results
    previous_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    prcp_results = session.query(measurement.date,measurement.prcp).filter(measurement.date>=previous_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a list of the last year of temperature data
    previous_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    temp_results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station=='USC00519281').filter(measurement.date>=previous_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of temp_dates
    temp_dates = []
    for date, tobs in temp_results:
        passenger_dict = {}
        passenger_dict["date"] = date
        passenger_dict["tobs"] = tobs
        temp_dates.append(passenger_dict)

    return jsonify(temp_dates)


@app.route("/api/v1.0/<start>")
def start(start):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start_date = dt.datetime.strptime(start, "%m-%d-%Y")
    #Return a list of the data for that specific date
    temp_results= session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date>=start_date).all()
    session.close()

    # Create a dictionary from the row data and append to a list of onedate_temp
    onedate_temp = list(np.ravel(temp_results))

    return jsonify(onedate_temp)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start_date = dt.datetime.strptime(start, "%m-%d-%Y")
    end_date = dt.datetime.strptime(end, "%m-%d-%Y")
    
    #Return a list of averaged data between the two dates
    temp_results= session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date>=start_date).\
    filter(measurement.date<=end_date).all()
    session.close()

    # Create a dictionary from the row data and append to a list of avg_data
    avg_data = list(np.ravel(temp_results))

    return jsonify(avg_data)




if __name__ == '__main__':
    app.run(debug=True)