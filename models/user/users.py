from models.db import db
from models.user.roles import Role
from werkzeug.security import generate_password_hash 

class User(db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer(), primary_key=True)
    role_id = db.Column( db.Integer, db.ForeignKey(Role.id))
    username= db.Column(db.String(45) , nullable=False, unique=True)
    email= db.Column(db.String(30), nullable=False, unique=True)
    password= db.Column(db.String(256) , nullable=False)
    telefone = db.Column(db.String(45) , nullable=False)
    
    def save_user(role_type_, username, email,password, telefone):
        role = Role.get_single_role(role_type_)
        user = User(role_id = role.id, username = username, email = email, password = generate_password_hash(password), telefone = telefone)

        db.session.add(user)
        db.session.commit()

    def get_user():
        users = db.session.query(User).join(Role, User.role_id == Role.id).add_columns(
            User.id,
            User.username,
            User.email,
            User.telefone,
            Role.name.label("role_type_")
        ).all()
        return users
    
    def get_single_user(id):
        user = User.query.filter(User.id == id).first()

        if user is not None:
            user = User.query.filter(User.id == id)\
            .join(Role).add_columns(Role.id.label("role_id"), Role.name, Role.description, User.username,
                                     User.email, User.telefone, User.password, User.id).first()

        return [user]

    def update_user(id, username, email, role_type, telefone, password=None):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            role = Role.get_single_role(role_type)
            if role:
                user.username = username
                user.email = email
                user.role_id = role.id
                user.telefone = telefone
                
                if password:
                    user.password = generate_password_hash(password)
                    
                db.session.commit()
        return User.get_user()
    
    def delete_user(id):
        user = User.query.filter(User.id == id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        return User.get_user()
