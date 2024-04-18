
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SECRET_KEY'] = 'yoursecretkey'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity')
    cart.add(product, quantity)
    flash('Product added to cart.')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    return render_template('cart.html', cart=cart)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    product = Product.query.get_or_404(product_id)
    cart.remove(product)
    flash('Product removed from cart.')
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    order = Order(customer_name=request.form.get('customer_name'),
                  customer_email=request.form.get('customer_email'),
                  customer_address=request.form.get('customer_address'),
                  total=cart.total)
    db.session.add(order)
    db.session.commit()
    cart.clear()
    flash('Order placed successfully.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
