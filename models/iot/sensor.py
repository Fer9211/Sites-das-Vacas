from models.db import db
from models.iot.devices import Device
class Sensor(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    id_device = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=False)    
    topico_sensor = db.Column(db.String(150), nullable=True)

    def save_sensor(
            device_name, 
            marca, 
            modelo, 
            localizacao_fisica, 
            status_operacional, 
            topico_sensor):
        
        device = Device(
            device_name=device_name,
            marca = marca,
            modelo = modelo,
            localizacao_fisica=localizacao_fisica,
            status_operacional=status_operacional
        )

        sensor = Sensor(
            id_device = device.id,
            topico_sensor = topico_sensor
        )

        device.sensor.append(sensor)
        db.session.add(device)
        db.session.commit()

    def get_sensores():
        sensores = Sensor.query.join(Device, Device.id == Sensor.id_device)\
            .add_columns(Device.id, Device.device_name, Device.marca, 
                         Device.modelo, Device.localizacao_fisica, Device.status_operacional,
                          Sensor.topico_sensor).all()
        return sensores
    
    
    def get_single_sensor(id):
        sensor = Sensor.query.filter(Sensor.id_device == id).first()
        if sensor is not None:
            sensor = Sensor.query.filter(Sensor.id_device == id)\
                .join(Device).add_columns(Device.id, Device.device_name, Device.marca, 
                                            Device.modelo, Device.localizacao_fisica, 
                                            Device.status_operacional,
                                            Sensor.topico_sensor).first()
            return sensor
    
    def update_sensor(id,device_name, marca, modelo, localizacao_fisica, 
                       status_operacional, topico_sensor):
        sensor = Sensor.query.filter(Sensor.id_device == id).first()
        device = Device.query.filter(Device.id == id).first()
        if device is not None:
            device.device_name = device_name
            device.marca = marca
            device.modelo = modelo
            device.localizacao_fisica = localizacao_fisica
            device.status_operacional = status_operacional
            sensor.topico_sensor = topico_sensor 

            
            db.session.commit()
            return Sensor.get_sensores()
        
    def delete_sensor(id):
        sensor = Sensor.query.filter(Sensor.id_device == id).first()
        device = Device.query.filter(Device.id == id).first()
        
        db.session.delete(sensor)
        db.session.delete(device)
        db.session.commit()
        return Sensor.get_sensores()