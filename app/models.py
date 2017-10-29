from flask_sqlalchemy import SQLAlchemy
import logging as lg
from .views import app
import enum
# Main
db = SQLAlchemy(app)
db.create_all()
# Model
class Gender(enum.Enum):
    female = 0
    male = 1
    other = 2
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    def __init__(self, description, gender):
        self.description = description
        self.gender = gender
# Command
def test_command():
    db.session.add(Content("TEST1", Gender['male']))
    db.session.add(Content("TEST2", Gender['female']))
# Command
def recommend():
    return "Batman"
