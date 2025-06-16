from flask import Flask
from models.db import db
from models.user.users import User
from models.user.roles import Role
from werkzeug.security import generate_password_hash

def create_db(app: Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin_role = Role.query.filter_by(name='Admin').first()
        if not admin_role:
            admin_role = Role(name='Admin', description='Administrador do sistema com acesso total.')
            db.session.add(admin_role)
            db.session.commit()

        hashed_password = generate_password_hash("sua_senha_admin_muito_segura")

        admin_user = User(
            role_id=admin_role.id,
            username="admin",
            email="admin@seuprojeto.com",
            password=hashed_password,
            telefone="(XX) XXXXX-XXXX"
        )

        db.session.add(admin_user)
        db.session.commit()

        print("Banco de dados resetado e usuário 'admin' criado com sucesso!")