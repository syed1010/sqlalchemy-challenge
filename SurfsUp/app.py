# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


#################################################
# Database Setup
#################################################
app = Flask('climateap')

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    """Homepage route"""
    return (
        f"Welcome to the Climate App!<br/><br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    """Precipitation route"""
    session = Session(engine)
    # Calculate the date one year from the last date in data set
    one_year_ago = dt.date.today() - dt.timedelta(days=365)
    # Perform query to retrieve precipitation data for the last 12 months
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    session.close()
    # Convert query results to JSON format
    precipitation_json = [{"Date": date, "Precipitation": prcp} for date, prcp in precipitation_data]
    # Return JSON representation of precipitation data
    return jsonify(precipitation_json)

@app.route('/api/v1.0/stations')
def stations():
    """Stations route"""
    session = Session(engine)
    # Perform query to retrieve stations data
    stations_data = session.query(Station.station, Station.name).all()
    session.close()
    # Convert query results to JSON format
    stations_json = [{"Station ID": station, "Name": name} for station, name in stations_data]
    # Return JSON list of stations
    return jsonify(stations_json)

@app.route('/api/v1.0/tobs')
def tobs():
    """TOBS route"""
    session = Session(engine)
    # Determine the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count().desc()).first()[0]
    # Calculate the date one year from the last date in data set
    one_year_ago = dt.date.today() - dt.timedelta(days=365)
    # Perform query to retrieve temperature observations data for the previous year for the most active station
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()
    session.close()
    # Convert query results to JSON format
    tobs_json = [{"Date": date, "Temperature": tobs} for date, tobs in tobs_data]
    # Return JSON list of temperature observations
    return jsonify(tobs_json)

@app.route('/api/v1.0/<start>')
def start_date(start):
    """Start date route"""
    session = Session(engine)
    # Perform query to calculate temperature statistics for the specified start date
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    # Convert query results to JSON format
    temp_stats_json = {"TMIN": temp_stats[0][0], "TAVG": temp_stats[0][1], "TMAX": temp_stats[0][2]}
    # Return JSON list of temperature statistics
    return jsonify(temp_stats_json)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    """Start and end date route"""
    session = Session(engine)
    # Perform query to calculate temperature statistics for the specified date range
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    # Convert query results to JSON format
    temp_stats_json = {"TMIN": temp_stats[0][0], "TAVG": temp_stats[0][1], "TMAX": temp_stats[0][2]}
    # Return JSON list of temperature statistics
    return jsonify(temp_stats_json)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)