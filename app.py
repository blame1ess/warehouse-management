from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:26082001@localhost/commodities'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

app.app_context().push()

class Commodity(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    barcode = db.Column(db.String(100))
    amount = db.Column(db.String(100))
    buying_price = db.Column(db.Integer)
    selling_price = db.Column(db.Integer)
    revenue = db.Column(db.Integer)
    supplier = db.Column(db.String(100))

    def __init__(self, name, barcode, amount, buying_price, selling_price, revenue, supplier):
        self.name = name
        self.barcode = barcode
        self.amount = amount
        self.buying_price = buying_price
        self.selling_price = selling_price
        self.revenue = revenue
        self.supplier = supplier


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/warehouses')
def index():
    all_data = Commodity.query.all()
    return render_template('index.html', commodities = all_data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form.get('name')
        barcode = request.form.get('barcode')
        amount = request.form.get('amount')
        buying_price = request.form.get('buy')
        selling_price = request.form.get('sell')
        revenue = int(selling_price) - int(buying_price)
        supplier = request.form.get('supplier')

        my_data = Commodity(name, barcode, amount, buying_price, selling_price, revenue, supplier)
        db.session.add(my_data)
        db.session.commit()

        flash("Commodity added successfully")

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Commodity.query.get(request.form.get('id'))
        my_data.name = request.form.get('name')
        my_data.barcode = request.form.get('barcode')
        my_data.amount = request.form.get('amount')
        my_data.buying_price = request.form.get('buy')
        my_data.selling_price = request.form.get('sell')
        my_data.revenue = int(my_data.selling_price) - int(my_data.buying_price)
        my_data.supplier = request.form.get('supplier')

        db.session.commit()

        flash("Information updated successfully")

        return redirect(url_for('index'))


@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete(id):
    my_data = Commodity.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Commodity deleted successfully")
    return redirect(url_for('index'))

# sessions:



if __name__ == "__main__":
    app.run(port=9000, debug=True)