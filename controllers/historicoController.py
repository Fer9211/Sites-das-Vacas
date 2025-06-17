from flask import Blueprint, request, render_template, redirect, url_for
from utils.decorators import role_required
from models.db import db
from sqlalchemy import text

historico = Blueprint("historico_blueprint", __name__, template_folder="templates")

@historico.route('/historicos')
@role_required(roles=['Admin', 'Veterinario','Funcionario'])
def listar_historico():  # ✅ Nome diferente do blueprint
    historico_data = db.session.execute(text("""
    SELECT 
        d.horario AS data_hora,
        d.peso AS quantidade_definida,
        s.valor_umidade AS umidade,
        bl.peso AS peso_restante
    FROM despejo d
    LEFT JOIN sensor_leituras s ON s.id_device = (
        SELECT id_device FROM sensor ORDER BY id DESC LIMIT 1
    )
    LEFT JOIN balanca_leituras bl ON bl.id_device = (
        SELECT id_device FROM balanca ORDER BY id DESC LIMIT 1
    )
    ORDER BY d.horario DESC
    LIMIT 10;
""")).fetchall()

    return render_template('historico.html', historico=historico_data)
