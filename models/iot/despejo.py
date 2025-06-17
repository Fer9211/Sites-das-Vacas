import datetime
from models.db import db

class Despejo(db.Model):
    __tablename__ = 'despejo'

    id = db.Column(db.Integer, primary_key=True)
    peso = db.Column(db.Float, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
