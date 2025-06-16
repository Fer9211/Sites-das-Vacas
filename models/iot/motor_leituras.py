from models.db import db
from models.iot.devices import Device
import datetime

class MotorLeituras(db.Model):
    __tablename__ = 'motor_leituras'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_motor = db.Column(db.Enum('Aberto', 'Fechado'), nullable=False)
    id_device = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    motor_datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    device = db.relationship('Device', backref=db.backref('motor_leituras', lazy=True))
