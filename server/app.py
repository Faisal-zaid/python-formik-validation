from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import Customer, db

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Routes
@app.route("/customers", methods=['GET', 'POST'])
def customers():
    if request.method == 'GET':
        all_customers = [customer.to_dict() for customer in Customer.query.all()]
        return make_response(jsonify(all_customers), 200)

    if request.method == 'POST':
        data = request.get_json()
        customer = Customer(
            name=data.get('name'),
            email=data.get('email'),
            age=data.get('age')
        )
        db.session.add(customer)
        db.session.commit()
        
        response_data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'age': customer.age
        }
        return make_response(jsonify(response_data), 201)

@app.route("/customers/<int:id>", methods=['PATCH', 'DELETE'])
def customer_by_id(id):
    customer = Customer.query.get_or_404(id)

    if request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
        db.session.commit()
        return make_response(jsonify(customer.to_dict()), 200)

    if request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return make_response(jsonify({'deleted': True}), 200)

# Run the app
if __name__ == "__main__":
    app.run(port=5555, debug=True)