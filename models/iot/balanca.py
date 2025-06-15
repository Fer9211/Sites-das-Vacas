from models import db
from models.iot.devices import Device

class Balanca(db.Model):
    __tablename__ = 'balanca'

    id = db.Column(db.Integer, primary_key=True)
    id_device = db.Column(db.Integer, db.ForeignKey(Device.id))
    topico_balanca = db.Column(db.String(100), nullable=True)


    def save_balanca(
            device_name, 
            marca,  
            modelo, 
            localizacao_fisica, 
            status_operacional, 
            topico_balanca):
        
        device = Device(
            device_name=device_name,
            marca = marca,
            modelo = modelo,
            localizacao_fisica=localizacao_fisica,
            status_operacional=status_operacional
        )

        balanca = Balanca(
            id_device=device.id,
            topico_balanca=topico_balanca
        )
    
        device.balanca.append(balanca)
        db.session.add(device)
        db.session.commit()
        

    def get_balancas():
        balancas = Balanca.query.join(Device, Device.id == Balanca.id_device)\
            .add_columns(Device.id, Device.device_name, Device.marca, Device.modelo, Device.localizacao_fisica, Device.status_operacional,
                          Balanca.topico_balanca).all()
        return balancas
    
    def get_single_balanca(id):
        balanca = Balanca.query.filter(Balanca.id_device == id).first()
        if balanca is not None:
            balanca = Balanca.query.filter(Balanca.id_device == id)\
                .join(Device).add_columns(Device.id, Device.device_name, Device.marca, 
                                          Device.modelo, Device.localizacao_fisica, 
                                          Device.status_operacional,
                                          Balanca.topico_balanca).first()
            return balanca
        
    def update_balanca(id,device_name, marca, modelo, localizacao_fisica, 
                       status_operacional, topico_balanca):
        balanca = Balanca.query.filter(Balanca.id_device == id).first()
        device = Device.query.filter(Device.id == id).first()
        if device is not None:
            device.device_name = device_name
            device.marca = marca
            device.modelo = modelo
            device.localizacao_fisica = localizacao_fisica
            device.status_operacional = status_operacional
            balanca.topico_balanca = topico_balanca 

            
            db.session.commit()
            return Balanca.get_balancas()
        
    def delete_balanca(id):
        balanca = Balanca.query.filter(Balanca.id_device == id).first()
        device = Device.query.filter(Device.id == id).first()
        
        db.session.delete(balanca)
        db.session.delete(device)
        db.session.commit()
        return Balanca.get_balancas()