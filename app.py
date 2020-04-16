from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap 
import pandas as pd 
import numpy as np 
# import matplotlib.pyplot as plt
import pickle

# ML Packages
# from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.model_selection import train_test_split

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # df1 = pd.read_csv("wine-reviews/winemag-data-130k-v2.csv")
    # parsed_data = df1[df1.duplicated('description', keep=False)].copy()
    # parsed_data.dropna(subset=['description', 'points', 'price', 'country'], inplace=True)
    # df2 = parsed_data[['description','points','price', 'country']]

    # 1 -> Points 80 to 84 (Under Average wines)

    # 2 -> Points 84 to 88 (Average wines)

    # 3 -> Points 88 to 92 (Good wines)

    # 4 -> Points 92 to 96 (Very Good wines)

    # 5 -> Points 96 to 100 (Excellent wines)

    #Transform method taking points as param
    def transform_points_simplified(points):
        if points < 84:
            return 1
        elif points >= 84 and points < 88:
            return 2 
        elif points >= 88 and points < 92:
            return 3 
        elif points >= 92 and points < 96:
            return 4 
        else:
            return 5

    #Applying transform method and assigning result to new column "points_simplified"
    # df2 = df2.assign(points_simplified = df2['points'].apply(transform_points_simplified))
 	# # Features and Labels
    # df2['finaltextinput'] = df2['description'] + ' ' + df2['country']
    # def lower_all(input_string):
    #     return input_string.lower()

    # df2["finaltextinput"] = df2["finaltextinput"].apply(lower_all)

    # X = df2['finaltextinput']
    # y = df2['points_simplified']
    # X2 = df2['price']
    
    # Vectorization
    # vectorizer = CountVectorizer()
    # vectorizer.fit(X)
    # X = vectorizer.transform(X)
    # pd.DataFrame.sparse.from_spmatrix(X)
    # X2.reset_index(drop = True, inplace = True)
    # Z =pd.DataFrame.sparse.from_spmatrix(X).join(X2)
	
    with open('models/winevect_model.pickle', 'rb') as handle:
        loaded_vec = pickle.load(handle)



 	# # Loading our ML Model
    # RandomForestClassifier_model = open("models/wine_rfc_model.pickle","rb")
    # rfc = joblib.load(RandomForestClassifier_model)

    with open('models/wine_rfc_model.pickle', 'rb') as handle:
        rfc = pickle.load(handle)


 	# Receives the input query from form
    if request.method == 'POST':
        namequery = request.form['namequery']
        countryquery = request.form['country']
        namequery = namequery + " " + countryquery
        data = [namequery]
        X_example = loaded_vec.transform(data)
        input_price = request.form['price']
        if not( isinstance(input_price, float) or isinstance(input_price, int)):
            print("expected a number")
        data_price = [input_price]

        X2_example = pd.Series(input_price, name = "price")
        pd.DataFrame.sparse.from_spmatrix(X_example)
        X2_example.reset_index(drop = True, inplace = True)
        Z_example =pd.DataFrame.sparse.from_spmatrix(X_example).join(X2_example)
# 		vect = cv.transform(data).toarray()
# 		my_prediction = clf.predict(vect)
        my_prediction = rfc.predict(Z_example)
    return render_template('results.html',prediction = my_prediction,name = namequery.upper())


if __name__ == '__main__':
	app.run(debug=True)