from models import db

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column('id', db.Integer, primary_key=True)
    device_name = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    localizacao_fisica = db.Column(db.String(100))
    status_operacional = db.Column(db.Enum('Online', 'Offline'), default='Offline', nullable=False)
    balanca = db.relationship('Balanca', backref='devices', lazy=True)
    motor = db.relationship('Motor', backref='devices', lazy=True)
    sensor = db.relationship('Sensor', backref='devices', lazy=True)
