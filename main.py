from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wirehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.Float)


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    quantity = db.Column(db.Integer)


@app.route('/', methods=['POST', 'GET'])
def index():
    products = Products.query.order_by(Products.id).all()
    return render_template('index.html', products=products)


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        name = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        
        product = Products(name=name, description=description, price=price)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка при добавлении продукта'
    else:
        return render_template('add_product.html')


@app.route('/add_location', methods=['POST', 'GET'])
def add_location():
    if request.method == 'POST':
        name = request.form['title']
        product = Locations(name=name)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка при добавлении локации'
    else:
        return render_template('add_location.html')


if __name__ == '__main__':
    app.run(debug=True)
