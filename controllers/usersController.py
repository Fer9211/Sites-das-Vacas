from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from utils.decorators import role_required
from models.user.users import User 
from models.user.roles import Role
from werkzeug.security import check_password_hash

user = Blueprint("user_blueprint", __name__, template_folder="templates")

@user.route('/login', methods=['GET', 'POST'])
def login():  
    if request.method == 'POST':
        username_form = request.form['user']
        password_form = request.form['password']

        user_db = User.query.filter_by(username=username_form).first()

        if user_db and check_password_hash(user_db.password, password_form):
            user_role = Role.query.get(user_db.role_id)
            session['user_id'] = user_db.id
            session['username'] = user_db.username
            session['role'] = user_role.name
            return redirect(url_for('dadosAtuais_blueprint.dadoAtual'))
        else:
            return redirect(url_for('user_blueprint.login'))

    return render_template('login.html')

@user.route('/logout')
def logout():
    session.clear() 
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('user_blueprint.login'))
    
@user.route('/add_user', methods=['POST'])
@role_required(roles=['Admin']) 
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        telefone = request.form['telefone']
        password = request.form['senha']
        role_id = request.form['role_id']

        if User.query.filter_by(username=username).first():
            flash(f'O nome de usuário "{username}" já está em uso.', 'danger')
            return redirect(url_for('user_blueprint.cadastrarUser'))
        
        if User.query.filter_by(email=email).first():
            flash(f'O email "{email}" já está cadastrado.', 'danger')
            return redirect(url_for('user_blueprint.cadastrarUser'))
        
        role = Role.query.get(role_id)
        if not role:
            flash('Função (role) inválida selecionada.', 'danger')
            return redirect(url_for('user_blueprint.cadastrarUser'))

        User.save_user(role_type_=role.name, username=username, email=email, password=password, telefone=telefone)

        flash(f'Usuário {username} cadastrado com sucesso!', 'success')
        return redirect(url_for('user_blueprint.listarUser'))

    return redirect(url_for('user_blueprint.cadastrarUser'))


@user.route('/cadastrarUser')
@role_required(roles=['Admin'])
def cadastrarUser():
    roles = Role.query.all()
    return render_template('cadastrarUser.html', roles=roles)

@user.route('/listarUser')
@role_required(roles=['Admin', 'Funcionario']) 
def listarUser():
    users_from_db = User.get_user()
    return render_template('usuarios.html', users=users_from_db)

@user.route("/editarUsuario/<int:id>")
@role_required(roles=['Admin'])
def editarUsuario(id):
    user_data = User.get_single_user(id)[0] 
    all_roles = Role.query.all()

    if not user_data:
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('user_blueprint.listarUser'))

    return render_template('editarUsuario.html', user=user_data, roles=all_roles)


@user.route("/update_user/<int:id>", methods=['POST'])
@role_required(roles=['Admin'])
def update_user(id):
    username = request.form['username']
    email = request.form['email']
    telefone = request.form['telefone']
    role_id = request.form['role_id']
    password = request.form['password'] 
    
    role = Role.query.get(role_id)
    
    User.update_user(id, username, email, role.name, telefone, password)

    flash('Usuário atualizado com sucesso!', 'success')
    return redirect(url_for('user_blueprint.listarUser'))

@user.route('/delete_user/<int:id>')
@role_required(roles=['Admin'])
def delete_user(id):
    User.delete_user(id)
    
    return redirect(url_for('user_blueprint.listarUser'))
