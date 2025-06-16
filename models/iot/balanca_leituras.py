from models import db
from models.iot.devices import Device

class BalancaLeituras(db.Model):
    __tablename__ = 'balanca_leituras'

    id = db.Column(db.Integer, primary_key=True)
    id_device = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=True)
    peso = db.Column(db.Float, nullable=False)
    peso_datetime = db.Column(db.DateTime, nullable=False)

    device = db.relationship('Device', backref='balanca_leituras')
