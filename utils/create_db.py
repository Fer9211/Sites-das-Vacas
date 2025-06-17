from flask import Flask
from models.db import db
from models.user.users import User
from models.user.roles import Role
from werkzeug.security import generate_password_hash

def create_db(app: Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()

        roles = ['Admin', 'Funcionario', 'Veterinario']
        descriptions = {
            'Admin': 'Administrador do sistema com acesso total.',
            'Funcionario': 'Funcionário com acesso a operações do dia-a-dia.',
            'Veterinario': 'Veterinário com acesso a dados de saúde e relatórios.'
        }

        for role_name in roles:
            if not Role.query.filter_by(name=role_name).first():
                role = Role(name=role_name, description=descriptions[role_name])
                db.session.add(role)
        
        db.session.commit()
        admin_role = Role.query.filter_by(name='Admin').first()
        if not User.query.filter_by(username='admin').first():
            hashed_password = generate_password_hash("1234") 

            admin_user = User(
                role_id=admin_role.id,
                username="admin",
                email="admin@gmail.com",
                password=hashed_password,
                telefone="(99) 99999-9999"
            )
            db.session.add(admin_user)
            db.session.commit()
            print(" Usuário 'admin'  criado com sucesso!")
