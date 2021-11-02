from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from requestcode import asin_from_url, get_date, get_info, url_from_asin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3211@localhost/product'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

app.config['CELERY_BACKEND'] = "redis://localhost:6379/0"
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/0"

class Product(db.Model):
    product_id = db.Column(db.String(100), primary_key=True, unique=True) 
    asin = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    search_date = db.Column(db.DateTime)
    price = db.Column(db.Float(20), nullable=False)
    rating = db.Column(db.Float(10), nullable=False)

def add_products(product_id, asin, title, url, search_date, price, rating):
    product = Product(
        product_id = product_id,
        asin = asin,
        title = title,
        url = url,
        search_date = search_date,
        price = price,
        rating = rating
    )
    db.session.add(product)
    db.session.commit()

def check_in_database(asin,search_date):
    data = Product.query.filter_by(asin=asin, search_date=search_date).all()
    return bool(data)

def get_product(asin):
    data = Product.query.filter_by(asin=asin).order_by(Product.search_date.desc()).all()
    info_list=[]
    for item in data:
        info =[item.asin,item.search_date,item.price,item.rating,item.title]
        info_list.append(info)
    return info_list

def fetch_asin():
    asin = [product.asin for product in Product.query.all()]
    return asin 

def get_latest_price(asin,search_date):
    price = Product.query.filter_by(asin=asin, search_date=search_date).order_by(Product.search_date.desc()).first().price
    return price





@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        asin = asin_from_url(url)
        search_date = get_date()
        available = check_in_database(asin,search_date)
        if available:
            data = get_product(asin)
            return render_template('index.html',da=data,ur=url_from_asin(asin))
        if not available:
            data = get_info(url)
            product_id, asin, title, url, search_date, price, rating = tuple(data.values())
            add_products(product_id, asin, title, url, search_date, price, rating)
            data = get_product(asin)
            return render_template('index.html',da=data,ur=url_from_asin(asin))
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)