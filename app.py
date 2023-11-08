"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from models import db, connect_db, Cupcake

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'

with app.app_context():
    connect_db(app)
    db.create_all()
    new_cupcake1 = Cupcake(flavor="Chocolate", size="large", rating=5, image="https://www.freeiconspng.com/uploads/birthday-cake-cupcake-food-icon--1.png")
    db.session.add(new_cupcake1)
    db.session.commit()
    new_cupcake2 = Cupcake(flavor="Vanilla", size="mini", rating=4, image="https://www.freeiconspng.com/uploads/birthday-cake-cupcake-food-icon--1.png")
    db.session.add(new_cupcake2)
    db.session.commit()
    new_cupcake2 = Cupcake(flavor="Caramel", size="large", rating=5, image="https://www.freeiconspng.com/uploads/birthday-cake-cupcake-food-icon--1.png")
    db.session.add(new_cupcake2)
    db.session.commit()

    
@app.route("/")
def root():
    """Homepage."""
    return render_template("index.html")


@app.route("/cupcakes")
def show_cupcakes_gallery():
    """Get data about all cupcakes."""

    # **GET /api/cupcakes :** Get data about all cupcakes. Respond with JSON like: 
    # `{cupcakes: [{id, flavor, size, rating, image}, ...]}`. The values should come from each cupcake instance.
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/cupcakes/<int:cupcake_id>")
def get_cupcake_data(cupcake_id):
    """Get data about a single cupcake."""
    
    # **GET /api/cupcakes/*[cupcake-id] :*** Get data about a single cupcake. Respond with JSON like: 
    # `{cupcake: {id, flavor, size, rating, image}}`. This should raise a 404 if the cupcake cannot be found.
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())
   
    
@app.route("/cupcakes", methods=["POST"])
def create_cupcake():
    """Create a cupcake."""
    
    # **POST /api/cupcakes :** Create a cupcake with flavor, size, rating and image data from the body of the request. 
    # Respond with JSON like: `{cupcake: {id, flavor, size, rating, image}}`.
    try:
        data = request.json
        new_cupcake = Cupcake(
            flavor=data["flavor"],
            size=data["size"],
            rating=data["rating"],
            image=data.get("image", "default_image_url")
        )

        db.session.add(new_cupcake)
        db.session.commit()

        return jsonify(cupcake=new_cupcake.to_dict()), 201
    except Exception as e:
        # In a production app, you might want to log this error.
        return jsonify(error=str(e)), 500
    
    
@app.route("/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake."""
    
    # **PATCH /api/cupcakes/*[cupcake-id] :*** Update a cupcake with the id passed in the URL and flavor, size, 
    # rating and image data from the body of the request. You can always assume that the entire cupcake object will be 
    # passed to the backend. This should raise a 404 if the cupcake cannot be found. 
    # Respond with JSON of the newly-updated cupcake, like this: `{cupcake: {id, flavor, size, rating, image}}`.
    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = data["flavor"]
    cupcake.size = data["size"]
    cupcake.rating = data["rating"]
    cupcake.image = data["image"]
    
    db.session.add(cupcake)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    # **DELETE /api/cupcakes/*[cupcake-id] :*** This should raise a 404 if the cupcake cannot be found.
    # Delete cupcake with the id passed in the URL. Respond with JSON like `{message: "Deleted"}`.
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()


