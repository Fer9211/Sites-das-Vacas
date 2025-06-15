
from flask import Flask, render_template
from models.db import db, instance

def create_app():

    app = Flask(
        __name__,
        template_folder="./templates/",  
        static_folder="./static/",     
        root_path="./"                 
    )


    app.config['SQLALCHEMY_DATABASE_URI'] = instance

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_forte_e_segura'

    
    # Isso é crucial e deve acontecer antes de qualquer modelo que use 'db.Model' ser importado ou definido
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template("login.html")

    return app
