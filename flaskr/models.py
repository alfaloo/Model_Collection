from flask_sqlalchemy import SQLAlchemy

# flask db init
# flask db migrate -m "Description of the changes"
# flask db upgrade

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32), nullable=False)
    make = db.Column(db.String(32), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    variant = db.Column(db.String(32), nullable=False)
    serial_number = db.Column(db.Integer, nullable=True)
    production_count = db.Column(db.Integer, nullable=True)
    purchase_price = db.Column(db.Integer, nullable=False)
    purchase_platform = db.Column(db.String(32), nullable=False)
    purchase_year = db.Column(db.Integer, nullable=False)
    purchase_month = db.Column(db.Integer, nullable=False)
    is_sold = db.Column(db.Boolean, nullable=False)
    sold_price = db.Column(db.Integer, nullable=True)
    sold_platform = db.Column(db.String(32), nullable=True)
    sold_year = db.Column(db.Integer, nullable=True)
    sold_month = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Item {self.id}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    category = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}>'