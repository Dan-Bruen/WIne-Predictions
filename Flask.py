# Flask.py
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Import scrapting dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import functools
import operator
from datetime import date
import time
from flask_cors import CORS
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///wines.sqlite")
print(engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Wine = Base.classes.wines

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)

@app.route("/api/v1.0/wines")
def wines():
     # Create our session (link) from Python to the DB
     session = Session(engine)

     """Return a list of all wines"""
     # Query all passengers
     results = session.query(Wine).all()

     df = pd.DataFrame([(d.index, d.description, d.points, d.price, d.country, for d in results], columns=['index', 'description', 'points', 'price', 'country'])
     data = df.to_dict('records')
     session.close()

     # Convert list of tuples into normal list

     return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)