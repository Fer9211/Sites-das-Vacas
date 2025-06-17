import datetime as dt # Importa o módulo datetime como 'dt' para evitar conflitos
from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.despejo import Despejo
from models.db import db

despejos = Blueprint("despejos_blueprint", __name__, template_folder="templates")

@despejos.route('/despejos')
def listar_despejos():
    # Busca todos os despejos ordenados pela data_hora (mais recente primeiro)
    # CORREÇÃO: Usar 'Despejo.data_hora' para ordenação.
    despejos_registrados = Despejo.query.order_by(Despejo.data_hora.desc()).all()
    return render_template('dadosAtuais.html', despejos=despejos_registrados)


@despejos.route('/cadastrar_despejo', methods=['POST'])
def cadastrar_despejo():
    peso = request.form.get('peso')
    # O nome do campo no formulário que envia APENAS a hora (ex: "03:26")
    horario_str = request.form.get('horario') # Assumindo que o nome do campo é 'horario'

    # Verifica se os dois foram enviados e são válidos
    if peso and horario_str:
        try:
            peso_float = float(peso)
            
            # 1. Obter a data atual do servidor
            today = dt.date.today() # CORREÇÃO: Usar dt.date.today()
            
            # 2. Tentar parsear a string de horário (ex: "03:26")
            # Supondo que o formato da hora seja HH:MM
            try:
                # Cria um objeto datetime temporário para extrair a hora e minuto
                temp_time = dt.datetime.strptime(horario_str, '%H:%M').time() # CORREÇÃO: Usar dt.datetime.strptime()
            except ValueError:
                print(f"Erro ao parsear o horário: {horario_str}. Usando 00:00 como hora.")
                temp_time = dt.datetime.min.time() # CORREÇÃO: Usar dt.datetime.min.time()
            
            # 3. Combinar a data atual com a hora parseada
            final_datetime = dt.datetime.combine(today, temp_time) # CORREÇÃO: Usar dt.datetime.combine()
            
            # Cria a nova instância de Despejo com a data e hora combinadas
            # CORREÇÃO: Passar para o argumento 'data_hora' do construtor Despejo
            novo_despejo = Despejo(peso=peso_float, data_hora=final_datetime)
            
            db.session.add(novo_despejo)
            db.session.commit()
        except ValueError as e: # Capture o erro para debug mais fácil
            # Tratamento se peso não for número válido
            print(f"Erro ao converter peso para float: {peso}. Detalhes: {e}")
            pass
    else:
        # Se um dos campos estiver faltando
        print(f"Erro: Peso ou horário faltando. Peso: {peso}, Horário: {horario_str}")
        pass

    return redirect(url_for('despejos_blueprint.listar_despejos'))
