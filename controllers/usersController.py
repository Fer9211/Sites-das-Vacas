from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from utils.decorators import role_required

user = Blueprint("user_blueprint", __name__, template_folder="templates")

users = {
    'admin': {'password': '1234', 'role': 'admin'},
    'veterinario':   {'password': '1234', 'role': 'veterinario'},
    'funcionario':  {'password': '1234', 'role': 'funcionario'}
}
@user.route('/validated_user', methods=['GET','POST'])
def validated_user():
    if request.method == 'POST':
        user_form = request.form['user']
        password = request.form['password']
        if user_form in users and users[user_form]['password'] == password:
            
            session['user_id'] = user_form
            session['role'] = users[user_form]['role']
            
            flash(f'Bem-vindo, {user_form}!', 'success')
            return redirect(url_for('dadosAtuais_blueprint.dadoAtual')) 

        else:
            flash('Usuário ou senha inválidos!', 'danger')
            return redirect(url_for('user_blueprint.validated_user')) 
    
    return render_template('login.html')

@user.route('/logout')
def logout():
    session.clear() 
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('user_blueprint.validated_user'))
    
@user.route('/cadastrarUser')
@role_required(roles=['admin'])
def cadastrarUser():
    return render_template('cadastrarUser.html')

@user.route('/listarUser')
@role_required(roles=['admin','funcionario'])
def listarUser():
    return render_template('usuarios.html')

@user.route("/editarUsuario")
@role_required(roles=['admin'])
def editarUsuario():
    return render_template('editarUsuario.html')
