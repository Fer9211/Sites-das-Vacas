from flask import Blueprint, request, render_template, redirect, url_for
from utils.decorators import role_required

dadosAtuais = Blueprint("dadosAtuais_blueprint", __name__, template_folder="templates")

@dadosAtuais.route('/dadoAtual')
@role_required(roles=['Admin', 'Funcionario', 'Veterinario'])
def dadoAtual():
    return render_template('dadosAtuais.html')
