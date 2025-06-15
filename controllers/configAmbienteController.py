from flask import Blueprint, request, render_template, redirect, url_for
from utils.decorators import role_required

configAmbientes = Blueprint("configAmbiente_blueprint", __name__, template_folder="templates")

@configAmbientes.route('/configAmbiente')
@role_required(roles=['admin', 'veterinario'])
def configAmbiente():
    return render_template('configAmbiente.html')
