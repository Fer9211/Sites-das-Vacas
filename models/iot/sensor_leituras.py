from models.db import db
from datetime import datetime

class SensorLeituras(db.Model):
    __tablename__ = 'sensor_leituras'

    id = db.Column(db.Integer, primary_key=True)
    id_device = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    sensor_datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)
    valor_umidade = db.Column(db.Float, nullable=False)
    status_umidade = db.Column(db.Enum('Bom', 'Alta', 'Baixa'), nullable=False)

    device = db.relationship('Device', backref='sensor_leituras')
