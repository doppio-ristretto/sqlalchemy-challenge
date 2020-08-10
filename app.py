import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app=Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
    )

@app.route ('/api/v1.0/precipitation')
def prcp():
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    bunch_o_stuff=[]
    for date,prcp in results:
        dict1={}
        dict1[date]=prcp
        bunch_o_stuff.append(dict1)
    return jsonify(bunch_o_stuff)

@app.route('/api/v1.0/stations')
def stations():
    session=Session(engine)
    results=session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route('/api/v1.0/tobs')
def tobs():
    session=Session(engine)
    lastdatestr=session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latestdate=dt.datetime.strptime(lastdatestr, '%Y-%m-%d')
    selecteddates=dt.date(latestdate.year -1, latestdate.month,latestdate.day)
    sel=[Measurement.date,Measurement.tobs]
    results=session.query(*sel).filter(Measurement.date >= selecteddates).all()
    session.close
    stuff_of_stuff=[]
    for date,tobs in results:
        dict2={}
        dict2['Date']=date
        dict2['tobs']=tobs
        stuff_of_stuff.append(dict2)
    return jsonify(stuff_of_stuff)


@app.route('/api/v1.0/<start>')
def starting(start):
    session=Session(engine)
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start_dt).all()
    session.close()
    allstarts=[]
    for result in results:
        dict3={}
        dict3["StartDate"] = start_dt
        dict3['TMIN']=result[0]
        dict3['TMAX']=result[1]
        dict3['TAVG']=result[2]
        allstarts.append(dict3)

    return jsonify(allstarts)


@app.route('/api/v1.0/<start>/<stop>')
def start_stop(start,stop):
    session = Session(engine)
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    stop_dt = dt.datetime.strptime(stop, "%Y-%m-%d")
    queryresult = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start_dt).filter(Measurement.date <= stop_dt).all()
    session.close()
    startstops = []
    for result in queryresult:
        dict4 = {}
        dict4['StartDate']=start_dt
        dict4['EndDate']=stop_dt
        dict4["TMIN"] = result[0]
        dict4["TMAX"] = result[1]
        dict4["TAVG"] = result[2]
        startstops.append(dict4)

    return jsonify(startstops)


if __name__ == "__main__":
    app.run(debug=True)

