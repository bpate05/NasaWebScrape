from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_data

# create an instance of Flask
app = Flask(__name__)

# setup PyMongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route('/')
def home():
    mars_data = mongo.db.mars_info.find_one()

    return render_template("index.html", mars_data = mars_data)

@app.route('/scrape')
def scrape():
    mars_info = mongo.db.mars_info
    mars_data = scrape_data()
    mars_info.update({}, mars_data, upsert=True)
 
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)