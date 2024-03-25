from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

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


@app.route('/', methods=['GET'])
def index():
    inventory = Inventory.query.all()
    return render_template('index.html', inventory=inventory)


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


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        name = request.form['title']
        description = request.form['description']
        price = request.form['price']
        location = request.form['location']
        quantity = request.form['quantity']

        product = Products(name=name, description=description, price=price)
        db.session.add(product)
        db.session.commit()

        inventory = Inventory(product_id=product.id,
                              location_id=db.session.query(Locations).filter(Locations.name == location).first().id,
                              quantity=quantity)
        db.session.add(inventory)
        db.session.commit()

        return redirect('/')
    else:
        locations = Locations.query.all()
        return render_template('add_product.html', locations=locations)


@app.route('/add_location', methods=['POST', 'GET'])
def add_location():
    if request.method == 'POST':
        name = request.form['title']
        if db.session.query(Locations).filter(Locations.name == name).first():
            return render_template('add_location.html', exist='true')
        location = Locations(name=name)
        try:
            db.session.add(location)
            db.session.commit()
            return redirect('/')
        except Exception as error:
            return f'Ошибка при добавлении локации {error}'
    else:
        return render_template('add_location.html')


if __name__ == '__main__':
    app.run(debug=True)
