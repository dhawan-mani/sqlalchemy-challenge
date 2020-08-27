import numpy as np
from datetime import date as dt 
import datetime as dt
from dateutil.relativedelta import relativedelta  
from sqlalchemy import and_
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func
from flask import Flask,jsonify
#Creating an engine by providing the correct path to it
engine = create_engine(f"sqlite:///Resources/hawaii.sqlite")

#Relect an existing database into a new model
Base=automap_base()

#Reflect the tables
Base.prepare(engine,reflect=True)
Base.classes.keys()
#Creating instances of the tables
Measurement = Base.classes.measurement
Station= Base.classes.station
session = Session(engine)
#Flask Setup
 
app = Flask(__name__)


 #####################################
 ######## Flask routes #########
 #####################################

@app.route('/')
def Welcome():
    return (
       
        f"Available routes are :<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/station<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start/<start><br>"
        f"/api/v1.0/start/end/<start>/<end><br>"
        f"Please provide the date in YYYY-MM-DD format."
    )



#Convert the query results to a dictionary using `date` as the key and `prcp` as the value
@app.route('/api/v1.0/precipitation')
def Precipitation():
    Last_Date = dt.date(2017, 8,23) + relativedelta(years=-1) 
    Query = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=Last_Date).order_by(Measurement.date).all()
   
    return jsonify(Query)

#### Return a JSON list of stations from the dataset.####
@app.route('/api/v1.0/station')
def station():
    Station_list = session.query(Station.station,Station.name).all()
    return jsonify(Station_list)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route('/api/v1.0/tobs')
def tobs():
    Last_Date = dt.date(2017, 8,23) + relativedelta(years=-1) 
    Most_Active_Station = session.query(Measurement.station,func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    Temp_Data = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.station==Most_Active_Station[0]).\
            filter(Measurement.date>=Last_Date).all()
    return jsonify({f"Most active station is :{Most_Active_Station[0]}":(Temp_Data)})


# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` 
# for all dates greater than and equal to the start date.

@app.route('/api/v1.0/start/<start_date>')
def Start(start_date):
    results = session.query(Measurement.date,func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start_date).group_by(Measurement.date).order_by(Measurement.date).all()
    list = []
    print("Temperature Analysis for the dates greater than or equal to the start date ")
    for temps in results:
        dict = {"Date":temps[0],"Minimum Temp":temps[1],"Average Temp":temps[2],"Maximum Temp":temps[3]}
        list.append(dict)

    return jsonify(list)
    

 # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
 # for dates between the start and end date inclusive.

@app.route('/api/v1.0/start/end/<start>/<end>')
def  StartEnd(start,end):
    Query = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(and_(Measurement.date>=start),(Measurement.date<=end)).group_by(Measurement.date).\
            order_by(Measurement.date).all()
        
    Final_list = []
    print("Temperature Analysis for the dates between the start date & end date")
    for data in Query:
        dict = {"Date":data[0],"Minimum Temperature" : data[1],"Average Temperature":data[2], "Maximum Temperature" : data[3]}
        Final_list.append(dict)
    return jsonify(Final_list)


if __name__ == '__main__':
    app.run(debug=True)