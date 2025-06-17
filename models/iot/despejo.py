from models.db import db

class Despejo(db.Model):
    __tablename__ = 'despejo'

    id = db.Column(db.Integer, primary_key=True)
    peso = db.Column(db.Float, nullable=False)
    horario = db.Column(db.String(10), nullable=False)  
