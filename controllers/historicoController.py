from flask import Blueprint, request, render_template, redirect, url_for
from utils.decorators import role_required

historico = Blueprint("historico_blueprint", __name__, template_folder="templates")

@historico.route('/historicos')
@role_required(roles=['admin', 'veterinario','funcionario'])
def historicos():
    return render_template('historico.html')
