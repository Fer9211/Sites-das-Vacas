from models.db import db
from models.iot.devices import Device

class Motor(db.Model):
    __tablename__ = 'motor'

    id = db.Column(db.Integer, primary_key=True)
    id_device = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=False)
    topico_motor = db.Column(db.String(150), nullable=True)

    

    def save_motor(
            device_name, 
            marca, 
            modelo, 
            localizacao_fisica, 
            status_operacional, 
            topico_motor):
        
        device = Device(
            device_name=device_name,
            marca = marca,
            modelo = modelo,
            localizacao_fisica=localizacao_fisica,
            status_operacional=status_operacional
        )

        motor = Motor(
            id_device=device.id,
            topico_motor = topico_motor
        )

        device.motor.append(motor)
        db.session.add(device)
        db.session.commit()

    def get_motores():
        motores = Motor.query.join(Device, Device.id == Motor.id_device)\
            .add_columns(Device.id, Device.device_name, Device.marca, 
                         Device.modelo, Device.localizacao_fisica, Device.status_operacional,
                          Motor.topico_motor).all()
        return motores
    
    def get_single_motor(id):
        motor = Motor.query.filter(Motor.id_device == id).first()
        if motor is not None:
            motor = Motor.query.filter(Motor.id_device == id)\
                .join(Device).add_columns(Device.id, Device.device_name, Device.marca, 
                                            Device.modelo, Device.localizacao_fisica, 
                                            Device.status_operacional,
                                            Motor.topico_motor).first()
            return motor
    
    def update_motor(id,device_name, marca, modelo, localizacao_fisica, 
                       status_operacional, topico_motor):
        motor = Motor.query.filter(Motor.id_device == id).first()
        device = Device.query.filter(Device.id == id).first()
        if device is not None:
            device.device_name = device_name
            device.marca = marca
            device.modelo = modelo
            device.localizacao_fisica = localizacao_fisica
            device.status_operacional = status_operacional
            motor.topico_motor = topico_motor 

            
            db.session.commit()
            return Motor.get_motores()
        
    def delete_motor(id):
        motor = Motor.query.filter(Motor.id_device == id).first()
        device = Device.query.filter(Device.id == id).first()
        
        db.session.delete(motor)
        db.session.delete(device)
        db.session.commit()
        return Motor.get_motores()