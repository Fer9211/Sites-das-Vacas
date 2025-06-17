from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.sensor import Sensor
from utils.decorators import role_required

dht = Blueprint("dht_blueprint", __name__, template_folder="templates")

@dht.route("/dhts")
@role_required(roles=['Admin', 'Veterinario', 'Funcionario'])
def dhts():
    sensores = Sensor.get_sensores()
    return render_template("dht.html", sensores = sensores)

@dht.route('/cadastrarDht')
@role_required(roles=['Admin'])
def cadastrarDht():
    return render_template('cadastrarDHT.html')

@dht.route('/add_sensor', methods=['POST'])
def add_sensor():
    device_name = request.form.get("device_name")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    topico_sensor = request.form.get("topico_sensor")
    localizacao_fisica = request.form.get("localizacao_fisica")
    status_operacional = request.form.get('status_operacional', 'Offline')

    Sensor.save_sensor(device_name, marca, modelo, localizacao_fisica, status_operacional, topico_sensor)

    
    return redirect(url_for('dht_blueprint.dhts'))

@dht.route("/editarDht")
@role_required(roles=['Admin'])
def editarDht():
    id = request.args.get('id', None)
    sensor = Sensor.get_single_sensor(id)
    return render_template("editarDht.html", sensor = sensor)

@dht.route('/update_sensor', methods=['POST'])
def update_sensor():
    id = request.form.get('id')
    device_name = request.form.get("device_name")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    topico_sensor = request.form.get("topico_sensor")
    localizacao_fisica = request.form.get("localizacao_fisica")
    status_operacional = request.form.get('status_operacional', 'Offline')

    sensores = Sensor.update_sensor(
        id, device_name, marca, modelo, localizacao_fisica,
        status_operacional, topico_sensor
    )

    return render_template("dht.html", sensores = sensores)

@dht.route('/del_sensor', methods=['GET'])
def del_sensor():
    id = request.args.get('id', None)
    sensores = Sensor.delete_sensor(id)
    return render_template("dht.html", sensores = sensores)
