import os

import pandas as pd
import numpy as np


from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo


app = Flask(__name__)


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/wine_reviews")

# insert local data file into Mongodb
# "Refereces/Datasets/winemag-data-130k-vs.json"
# refer to MongoDB homework on how to insert json into mongodb

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/data")
def load_data():
    # write a statement that finds all the items in the db and sets it to a variable
    wine_reviews = list(mongo.db.wineJson.find({"variety":"Pinot Noir"}))
    wine_counts = mongo.db.wineJson.count_documents({"variety":"Pinot Noir"})
    # render an index.html template and pass it the data you retrieved from the database
    # return render_template("index.html", wine_data = wine_reviews)
    return f"<p>{wine_reviews}</p> <p>{wine_counts}</p>"


@app.route("/variety")
def variety():
    """Return a list of grape names."""
    wine_grapes = mongo.db.wineJson.distinct("variety")
    # Return a list of the column names (sample names)
    return jsonify(wine_grapes)

# @app.route("/data")
# def load_data():
#     # write a statement that finds all the items in the db and sets it to a variable
#     wine_reviews = list(mongo.db.wineJson.find({"variety":"Pinot Noir"}))
#     wine_counts = mongo.db.wineJson.count_documents({"variety":"Pinot Noir"})
#     # render an index.html template and pass it the data you retrieved from the database
#     # return render_template("index.html", wine_data = wine_reviews)
#     return f"<p>{wine_reviews}</p> <p>{wine_counts}</p>"

@app.route("/samples/<sample>")
def samples(sample):
    wine_reviews = list(mongo.db.wineJson.find({"variety":sample},{"_id":0}).limit(500))


    return jsonify(wine_reviews)

    # """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    # stmt = db.session.query(Samples).statement
    # df = pd.read_sql_query(stmt, db.session.bind)

    # # Filter the data based on the sample number and
    # # only keep rows with values above 1
    # sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

    # # Sort by sample
    # sample_data.sort_values(by=sample, ascending=False, inplace=True)

    # # Format the data to send as json
    # data = {
    #     "otu_ids": sample_data.otu_id.values.tolist(),
    #     "sample_values": sample_data[sample].values.tolist(),
    #     "otu_labels": sample_data.otu_label.tolist(),
    # }
    # return jsonify(data)








###########################





  # /sample is needed for wordcloud + bubble chart
    # only return the json data filtered by the grape
# import json

# input_json = """
# [
#     {
#         "type": "1",
#         "name": "name 1"
#     },
#     {
#         "type": "2",
#         "name": "name 2"
#     },
#     {
#         "type": "1",
#         "name": "name 3"
#     }
# ]"""

# # Transform json input to python objects
# input_dict = json.loads(input_json)

# # Filter python objects with list comprehensions
# output_dict = [x for x in input_dict if x['type'] == '1']

# # Transform python object back into json
# output_json = json.dumps(output_dict)

# # Show json
# print output_json

@app.route("/metadata/<sample>")
def sample_metadata1(sample):
    #metadata will be the first sample of the wine
    variety_chosen = dict(mongo.db.wineJson.find({"variety":sample},{"_id":0})[0])
    
    return jsonify(variety_chosen)


if __name__ == "__main__":
    app.run(debug=True)

