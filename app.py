from flask import Flask, render_template, url_for, request, redirect
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
    countrydropdown = ['France', 'US', 'Argentina', 'Italy', 'Chile', 'Germany',
       'Portugal', 'South Africa', 'Hungary', 'Australia', 'Spain',
       'Austria', 'New Zealand', 'Romania', 'Israel', 'Turkey', 'Greece',
       'Slovenia', 'Croatia', 'Georgia', 'England', 'Canada', 'Moldova',
       'Czech Republic', 'Bulgaria', 'Uruguay', 'Morocco', 'Mexico',
       'Lebanon', 'Brazil', 'Serbia', 'Switzerland', 'India',
       'Luxembourg', 'Cyprus', 'Macedonia']
    varietydropdown = ['Pinot Gris', 'Cabernet Sauvignon', 'Gewürztraminer', 'Chardonnay',
       'Malbec', 'Merlot', 'Pinot Noir', 'Gamay', 'Red Blend', 'Inzolia', 'Riesling', 'Sauvignon Blanc', 'Monica',
       'Bordeaux-style White Blend', 'Grillo', 'Syrah', 'Portuguese Red', 'Sangiovese', 'Tannat-Cabernet', 'Cabernet Franc', 'White Blend',
       'G-S-M', 'Zinfandel', 'Rhône-style Red Blend', 'Fumé Blanc', 'Furmint', 'Pinot Bianco', 'Syrah-Viognier', 'Shiraz', 'Rosé',
       'Tempranillo', 'Sparkling Blend', 'Grüner Veltliner', 'Grenache Blanc', 'Nebbiolo', 'Cortese', 'Champagne Blend',
       'Pinot Blanc', 'Glera', 'Pinot Grigio', 'Bonarda', 'Aglianico', 'Bordeaux-style Red Blend', 'Silvaner', 'Colombard',
       'Tempranillo Blend', 'Portuguese White', 'Tinta Miúda', 'Corvina, Rondinella, Molinara', "Nero d'Avola", 'Insolia',
       'Papaskarasi', 'Tannat-Syrah', 'Petite Sirah', 'Pinot Nero', 'Sherry', 'Greco', 'Viura', 'Viognier', 'Sauvignon', 'Sousão',
       'Port', 'Albariño', 'Vermentino', 'Turbiana', 'Barbera', 'Montepulciano', 'Agiorgitiko', 'Muscat', 'Malagousia',
       'Assyrtiko', 'Chenin Blanc', 'Sangiovese Grosso', 'Monastrell', 'Traminette', 'Melon', 'Sagrantino', 'Cesanese',
       'Touriga Nacional', 'Rosato', 'Rotgipfler', 'Tinta de Toro', 'Verdejo', 'Xarel-lo', 'Carmenère', 'Grenache', 'Meritage',
       'Vernaccia', 'Arinto', 'Friulano', 'Ribolla Gialla', 'Falanghina', 'Plavac Mali', 'Verdejo-Viura', 'Sauvignon Blanc-Semillon',
       'Saperavi', 'Altesse', 'Torrontés', 'Provence white blend', 'Alvarinho', 'Tinto Fino', 'Moschofilero', 'Cabernet Franc-Merlot',
       'Torbato', 'Garnacha', 'Syrah-Petit Verdot', 'Dolcetto', 'Pedro Ximénez', 'Verdicchio', 'Pinot Meunier', 'Pinotage',
       'Mourvèdre', 'Lagrein', 'Rosado', 'Malbec-Syrah', 'Garnacha Blanca', 'Feteascǎ Regalǎ', 'Cinsault',
       'Tempranillo-Cabernet Sauvignon', 'Cabernet Sauvignon-Tempranillo', 'Carignan', 'Cabernet-Syrah', 'Syrah-Grenache', 'Gamay Noir',
       'Feteasca Neagra', 'Rhône-style White Blend', 'Charbono', 'Garganega', 'Valdiguié', 'Vidal Blanc', 'Zibibbo', 'Mencía',
       'Uva di Troia', 'Petit Verdot', 'Nerello Mascalese', 'Graciano', 'Chardonnay-Sauvignon Blanc', 'Marsanne', 'Spätburgunder',
       'Petit Manseng', 'Blaufränkisch', 'Neuburger', 'Roter Veltliner', 'Syrah-Petite Sirah', 'Trincadeira', 'Rkatsiteli',
       'Austrian white blend', 'Syrah-Cabernet Sauvignon', 'Negroamaro', 'Lemberger', 'Aligoté', 'Xinomavro', 'Zweigelt',
       'Malvasia Istriana', 'Picpoul', 'Moscato', 'Arneis', 'Gelber Muskateller', 'Touriga Franca', 'Roussanne-Viognier', 
       'Malbec-Merlot', 'Gaglioppo', 'Ruché', 'Roussanne', 'Tannat', 'Dornfelder', 'Kalecik Karasi', 'Castelão',
       'Gros and Petit Manseng', 'Carricante', 'Carignane', 'Nerello Cappuccio', 'Verduzzo', 'Portuguese Sparkling', 'Fiano',
       'Portuguese Rosé', 'Godello', 'Primitivo', 'Lambrusco di Sorbara', 'Provence red blend', 'Cabernet Sauvignon-Syrah',
       "Cesanese d'Affile", 'Debit', 'Cabernet', 'Perricone', 'Posip', 'Syrah-Mourvèdre', 'Grenache-Mourvèdre', 'Weissburgunder',
       'Nero di Troia', 'Pinot-Chardonnay', 'Prosecco', 'Carmenère-Cabernet Sauvignon', 'Muskat Ottonel', 'Timorasso',
       'Pigato', 'Viognier-Gewürztraminer', 'Bobal', 'Malbec-Petit Verdot', 'Colombard-Ugni Blanc', 'St. Laurent',
       'Chardonnay-Semillon', 'Carignan-Grenache','Shiraz-Cabernet Sauvignon', 'Carignano', 'Marawi',
       'Chardonnay-Pinot Blanc', 'Cabernet Blend', 'Alicante Bouschet', 'Tinta Cao', 'Austrian Red Blend', 'Müller-Thurgau', 'Groppello',
       'Petite Verdot', 'Grenache-Shiraz', 'Traminer', 'Assyrtico', 'Kerner', 'Treixadura', 'Cabernet Sauvignon-Merlot', 'Muscatel',
       'Palomino', 'Orange Muscat', 'Tocai Friulano', 'Lambrusco', 'Sciaccerellu', 'Jacquère', 'Touriga Nacional-Cabernet Sauvignon',
       'Cabernet Sauvignon-Carmenère', 'Zierfandler', 'Touriga', 'Gros Manseng', 'Chardonnay-Viognier', 'Tempranillo-Shiraz',
       'Monastrell-Syrah', 'Seyval Blanc', 'Casavecchia', 'Trousseau Gris', 'Cabernet Sauvignon-Merlot-Shiraz', 'Durella',
       'Sangiovese-Syrah', 'Fer Servadou', 'Negrette', 'Mission', 'Colombard-Sauvignon Blanc', 'Syrah-Merlot', 'Lambrusco Salamino',
       'Lambrusco Grasparossa', 'Cannonau', 'Pecorino', 'Passerina', 'Moscatel', 'Malbec-Tannat', 'Grecanico', 'Kisi',
       'Pallagrello Nero', 'Loureiro', 'Verdelho', 'Refosco', 'Symphony', 'Teroldego', 'Cabernet Sauvignon-Sangiovese', 'Tamjanika',
       'Shiraz-Cabernet', 'Shiraz-Grenache', 'Tokay', 'Syrah-Cabernet Franc', 'Nosiola', 'Schiava',
       'Merlot-Cabernet Sauvignon', 'Muscat Canelli', 'Raboso', 'Viosinho', 'Sylvaner', 'Maria Gomes', 'Malbec-Cabernet Sauvignon',
       'Erbaluce', 'Grenache-Carignan', 'Chenin Blanc-Viognier', 'Muskat', 'Pansa Blanca', 'Tannat-Cabernet Franc', 'Pinot Noir-Gamay',
       'Grenache Blend', 'Prieto Picudo', 'Corvina', 'Souzao', 'Sémillon', 'Antão Vaz', 'Counoise', 'Alfrocheiro', 'Brachetto', 'Portuguiser',
       'Listán Negro', 'Tinto del Pais', 'Grolleau', 'Grauburgunder', 'Kekfrankos', 'Elbling', 'Alsace white blend', 'Pallagrello',
       'Trebbiano', 'Encruzado', 'Carignan-Syrah', 'Pinot Auxerrois', 'Carmenère-Syrah', 'Tinta Fina', 'Tempranillo-Garnacha',
       'Malvasia', 'Malvasia Nera', 'Other', 'Rieslaner', 'Chenin Blanc-Chardonnay', 'Emir', 'Merlot-Cabernet', 'Albarossa',
       'Black Muscat', 'Frappato', 'Baco Noir', 'Albana', 'Vidal', 'Aragonez', 'Uvalino', 'Sangiovese Cabernet', 'Garnacha-Syrah',
       'Cabernet Franc-Malbec', 'Bovale', 'Cabernet Sauvignon-Malbec', 'Hondarrabi Zuri', 'Cabernet Sauvignon-Shiraz', 'Baga',
       'Garnacha-Tempranillo', 'Coda di Volpe', 'Vignoles', 'Macabeo', 'Trepat', 'Aragonês', 'Siria', 'Chambourcin', 'Welschriesling',
       'Robola']
    return render_template('index.html', countrydropdown = countrydropdown, varietydropdown = varietydropdown)

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
	
    with open('models/winevect_rfc_model.pickle', 'rb') as handle:
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
        varietyquery = request.form['variety']
        namequery = namequery + " " + countryquery + " " + varietyquery
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