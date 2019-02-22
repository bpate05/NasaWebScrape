from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_data

# create an instance of Flask
app = Flask(__name__)

# setup PyMongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create database and collection which will store data
db = mongo.mars_db
collection = db.mars_data_coll

# Route to render index.html template using data from Mongo
@app.route('/')
def home():
    mars_data = collection.find_one()

    return render_template("index.html", mars_data = mars_data)

@app.route('/scrape')
def scrape():
    # execture web-scraping function and store results into variable
    db_data = scrape_data()

    # take results and store into mongoDB
    # collection.update({'id':1}, {"$set": mars_data}, upsert = True)
    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)