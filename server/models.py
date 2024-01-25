# Import necessary modules
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance
db = SQLAlchemy()

# Define Bakery model
class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    # Specify serialization rules
    serialize_rules = ('-baked_goods.bakery',)

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define relationship with BakedGood model
    baked_goods = db.relationship('BakedGood', backref='bakery')

    def to_dict(self):
        # Serialize Bakery and include nested BakedGoods
        return SerializerMixin.to_dict(self, nested={'baked_goods': BakedGood})

    def __repr__(self):
        return f'<Bakery {self.name}>'

# Define BakedGood model
class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    # Specify serialization rules
    serialize_rules = ('-bakery.baked_goods',)

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)  # Update to Float for price
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define foreign key relationship with Bakery model
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

    def to_dict(self):
        # Serialize BakedGood and include nested Bakery
        return SerializerMixin.to_dict(self, nested={'bakery': Bakery})

    def __repr__(self):
        return f'<Baked Good {self.name}, ${self.price:.2f}>'
