from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.motor import Motor
motor = Blueprint("motor_blueprint", __name__, template_folder="templates")

@motor.route('/motores')
def motores():
    motores = Motor.get_motores()
    return render_template("motor.html", motores = motores)

@motor.route('/cadastrarMotor')
def cadastrarMotor():
    return render_template('cadastrarMotor.html')

@motor.route('/add_motor', methods=['POST'])
def add_motor():
    device_name = request.form.get("device_name")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    topico_motor = request.form.get("topico_motor")
    localizacao_fisica = request.form.get("localizacao_fisica")
    status_operacional = request.form.get('status_operacional', 'Offline')

    Motor.save_motor(device_name, marca, modelo, localizacao_fisica, status_operacional, topico_motor)

    
    return redirect(url_for('motor_blueprint.motores'))

@motor.route("/editarMotor")
def editarMotor():
    id = request.args.get('id', None)
    motor = Motor.get_single_motor(id)
    return render_template("editarMotor.html", motor = motor)

@motor.route('/update_motor', methods=['POST'])
def update_motor():
    id = request.form.get('id')
    device_name = request.form.get("device_name")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    topico_motor = request.form.get("topico_motor")
    localizacao_fisica = request.form.get("localizacao_fisica")
    status_operacional = request.form.get('status_operacional', 'Offline')

    motores = Motor.update_motor(
        id, device_name, marca, modelo, localizacao_fisica,
        status_operacional, topico_motor
    )

    return render_template("motor.html", motores = motores)

@motor.route('/del_motor', methods=['GET'])
def del_sensor():
    id = request.args.get('id', None)
    motores = Motor.delete_motor(id)
    return render_template("motor.html", motores = motores)
