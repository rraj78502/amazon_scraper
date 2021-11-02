

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
    return data

def fetch_asin():
    asin = [product.asin for product in Product.query.all()]
    return asin 

def get_latest_price(asin,search_date):
    price = Product.query.filter_by(asin=asin, search_date=search_date).order_by(Product.search_date.desc()).first().price
    return price