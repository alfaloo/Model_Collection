from flask_sqlalchemy import SQLAlchemy

# flask db migrate -m "Description of the changes"
# flask db upgrade

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    sex = db.Column(db.String(16), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<Patient {self.name}>'

class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    category = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Diagnosis {self.id}>'