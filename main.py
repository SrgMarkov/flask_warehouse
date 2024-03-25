import logging

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    inventory = db.relationship('Inventory', backref='product', lazy='dynamic')


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), )
    inventory = db.relationship('Inventory', backref='location', lazy='dynamic')


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    quantity = db.Column(db.Integer)


def add_product(form_data):
    name = form_data['name'].lower()
    description = form_data['description']
    price = form_data['price']
    location = form_data['product_location']
    quantity = form_data['quantity']
    #TODO Add serializer for price and quantity

    product = Products(name=name, description=description, price=price)
    try:
        db.session.add(product)
        db.session.commit()
    except Exception as error:
         logger.error(f'Ошибка при добавлении продукта - {error}')

    inventory = Inventory(product_id=product.id,
                          location_id=db.session.query(Locations).filter(Locations.name == location).first().id,
                          quantity=quantity)
    try:
        db.session.add(inventory)
        db.session.commit()
    except Exception as error:
        logger.error(f'Ошибка при добавлении инвентаря -  {error}')


def add_location(form_data):
    name = form_data['location']
    if not db.session.query(Locations).filter(Locations.name == name).first():
        location = Locations(name=name)
        try:
            db.session.add(location)
            db.session.commit()
        except Exception as error:
            logger.error(f'Ошибка при добавлении локации {error}')


@app.route('/', methods=['GET', 'POST'])
def index():
    inventory = Inventory.query.all()
    locations = Locations.query.all()
    if request.method == 'POST':
        print(request.form)
        if 'name' in request.form:
            add_product(request.form)
            return redirect('/')
        if 'location' in request.form:
            add_location(request.form)
            return redirect('/')
        if 'search' in request.form:
            search = request.form['search'].lower()
            inventory = db.session.query(Inventory)\
                .join(Products, Products.id == Inventory.product_id)\
                .filter(Products.name.contains(search))
        if 'quantity_asc' in request.form:
            inventory = Inventory.query.order_by(Inventory.quantity).all()
        if 'quantity_desc' in request.form:
            inventory = Inventory.query.order_by(Inventory.quantity.desc()).all()
        if 'price_asc' in request.form:
            inventory = db.session.query(Inventory)\
                .join(Products, Products.id == Inventory.product_id)\
                .order_by(Products.price).all()
        if 'price_desc' in request.form:
            inventory = db.session.query(Inventory)\
                .join(Products, Products.id == Inventory.product_id)\
                .order_by(Products.price.desc()).all()
        if 'location-button' in request.form:
            location = request.form['location-button']
            inventory = db.session.query(Inventory) \
                .join(Locations, Locations.id == Inventory.location_id) \
                .filter(Locations.name.contains(location))
    return render_template('index.html', inventory=inventory, locations=locations)


@app.route('/add_count', methods=['POST'])
def add_count():
    position = db.session.query(Inventory).get(request.data.decode().split('=')[-1])
    position.quantity += 1
    db.session.commit()
    return jsonify(result='Количество позиций товара увеличено на 1')


@app.route('/delete_count', methods=['POST'])
def delete_count():
    position = db.session.query(Inventory).get(request.data.decode().split('=')[-1])
    if position.quantity != 0:
        position.quantity -= 1
        db.session.commit()
        return jsonify(result='Количество позиций товара уменьшено на 1')
    else:
        return jsonify(result='Количество позиций не может быть меньше 0')


if __name__ == '__main__':
    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger.setLevel(logging.ERROR)
    app.run(debug=True)
