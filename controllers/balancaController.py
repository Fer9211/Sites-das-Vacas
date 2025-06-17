from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.balanca import Balanca
from utils.decorators import role_required

balanca = Blueprint("balanca_blueprint", __name__, template_folder="templates")

@balanca.route('/balancas')
@role_required(roles=['Admin', 'Funcionario', 'Veterinario'])
def balancas():
    balancas = Balanca.get_balancas()
    return render_template('balanca.html', balancas = balancas)

@balanca.route('/cadastrarBalanca')
@role_required(roles=['Admin'])
def cadastrarBalanca():
    return render_template('cadastrarBalanca.html')

@balanca.route('/add_balanca', methods=['POST'])
def add_balanca():
    device_name = request.form.get("device_name")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    topico_balanca = request.form.get("topico_balanca")
    localizacao_fisica = request.form.get("localizacao_fisica")
    status_operacional = request.form.get('status_operacional', 'Offline')

    Balanca.save_balanca(device_name, marca, modelo, localizacao_fisica, status_operacional, topico_balanca)

    
    return redirect(url_for('balanca_blueprint.balancas'))

@balanca.route('/editarBalanca')
@role_required(roles=['Admin'])
def editarBalanca():
    id = request.args.get('id', None)
    balanca = Balanca.get_single_balanca(id)
    return render_template('editarBalanca.html', balanca = balanca)

@balanca.route('/update_balanca', methods=['POST'])
def update_balanca():
    id = request.form.get('id')
    device_name = request.form.get("device_name")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    topico_balanca = request.form.get("topico_balanca")
    localizacao_fisica = request.form.get("localizacao_fisica")
    status_operacional = request.form.get('status_operacional', 'Offline')

    balancas = Balanca.update_balanca(
        id, device_name, marca, modelo, localizacao_fisica,
        status_operacional, topico_balanca
    )

    return render_template("balanca.html", balancas = balancas)

@balanca.route('/del_balanca', methods=['GET'])
def del_balanca():
    id = request.args.get('id', None)
    balancas = Balanca.delete_balanca(id)
    return render_template("balanca.html", balancas = balancas)

