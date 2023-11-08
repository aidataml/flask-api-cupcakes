"""Model for Flask Cupcake App."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """Cupcake Database Model."""

    __tablename__ = "cupcakes"
    
    # ***id***: a unique primary key that is an auto-incrementing integer
    # ***flavor***: a not-nullable text column
    # ***size***: a not-nullable text column
    # ***rating***: a not-nullable column that is a float
    # ***image***: a non-nullable text column. If an image is not given, default to https://tinyurl.com/demo-cupcake

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    def to_dict(self):
        """Assign database columns to a dictionary of cupcake information."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }

def connect_db(app):
    """Connect to the cupcakes database."""

    db.app = app
    db.init_app(app)