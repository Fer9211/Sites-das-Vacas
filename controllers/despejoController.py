from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.despejo import Despejo
from models.db import db
despejos = Blueprint("despejos_blueprint", __name__, template_folder="templates")

@despejos.route('/despejos')
def listar_despejos():
    # Busca todos os despejos ordenados pelo horário (mais próximo primeiro)
    despejos = Despejo.query.order_by(Despejo.horario).all()
    return render_template('dadosAtuais.html', despejos=despejos)

@despejos.route('/cadastrar_despejo', methods=['POST'])
def cadastrar_despejo():
    peso = request.form.get('peso')
    horario = request.form.get('horario')

    # Verifica se os dois foram enviados e são válidos
    if peso and horario:
        try:
            peso_float = float(peso)
            novo_despejo = Despejo(peso=peso_float, horario=horario)
            db.session.add(novo_despejo)
            db.session.commit()
        except ValueError:
            # tratamento se peso não for número válido
            pass
    else:
        # Se quiser, pode tratar casos de só peso ou só horário aqui também,
        # ou rejeitar a requisição para que ambos sejam obrigatórios
        pass

    return redirect(url_for('despejos_blueprint.listar_despejos'))

