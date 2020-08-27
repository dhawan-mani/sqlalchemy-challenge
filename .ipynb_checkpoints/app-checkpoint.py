import numpy as np
import date as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import session
from sqlalchemy import create_engine,func
from flask import Flask,jsonify
#Creating an engine by providing the correct path to it
engine = create_engine(f"sqlite:///Resources/sqlite")

#Relect an existing database into a new model
Base=automap_base()

#Reflect the tables
Base.prepare(engine,reflect=True)

#Creating instances of the tables
Measurement = Base.classes.measurement()
Station= Base.classes.station()

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
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

if __name__ == '__main__':
    app.run(debug=True)