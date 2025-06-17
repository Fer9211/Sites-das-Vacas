import datetime
import json
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_mqtt import Mqtt
# Ensure these imports point to your actual models
from models.db import db, instance
from models.iot.balanca_leituras import BalancaLeituras
from models.iot.motor import Motor
from models.iot.motor_leituras import MotorLeituras
from models.iot.sensor_leituras import SensorLeituras

mqtt_client = Mqtt()

def create_app():
    app = Flask(
        __name__,
        template_folder="./templates/",
        static_folder="./static/",
        root_path="./"
    )

    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_forte_e_segura' # Remember to use a strong, secure key in production
    db.init_app(app)
    app.secret_key = 'chave-secreta'
    # --- Database Table Creation ---
    # This block ensures all tables defined in your models are created
    # if they don't already exist. It needs to run within an application context.
    with app.app_context():
        db.create_all()
        print("✅ Tabelas da base de dados verificadas/criadas.")
    # --- End Database Table Creation ---

    # MQTT Configuration
    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = '' # Add your MQTT username if required
    app.config['MQTT_PASSWORD'] = '' # Add your MQTT password if required
    app.config['MQTT_KEEPALIVE'] = 60
    app.config['MQTT_TLS_ENABLED'] = False

    mqtt_client.init_app(app)

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        """
        Handles the MQTT connection event.
        Subscribes to necessary topics upon successful connection.
        """
        print(f"✅ Conectado ao broker MQTT com status: {rc}")
        mqtt_client.subscribe('balanca/leitura')
        mqtt_client.subscribe('motor/status')
        mqtt_client.subscribe('sensor/umidade')
        # Add any other topics you need to subscribe to here

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        """
        Processes incoming MQTT messages based on their topic.
        It decodes the payload, parses it as JSON, extracts data,
        and saves it to the database. Includes robust error handling
        for payload parsing and missing data.
        """
        print(f"📥 Mensagem recebida no tópico {message.topic}: {message.payload}")
        try:
            payload_str = message.payload.decode('utf-8')
            parsed_payload = None # Will hold the dictionary or primitive value

            try:
                # Attempt to parse as JSON. This can return a dict, list, string, number, etc.
                parsed_payload = json.loads(payload_str)
            except json.JSONDecodeError:
                # If it's not valid JSON, it might be a simple value (like for sensor/umidade)
                if message.topic == 'sensor/umidade':
                    try:
                        # Convert to float directly if it's just the value
                        valor_umidade = float(payload_str)
                        # Create a dictionary structure to match the model expectation
                        # Use default values for id_device and status_umidade if they are not provided by the sensor
                        parsed_payload = {
                            'id_device': 'unknown_sensor_id', # Default or placeholder for sensors that only send value
                            'valor_umidade': valor_umidade,
                            'status_umidade': 'OK' # Default or placeholder
                        }
                        print(f"DEBUG: Payload 'sensor/umidade' processado como float. Payload sintético: {parsed_payload}")
                    except ValueError:
                        print(f"❌ Erro: Payload para sensor/umidade não é JSON válido nem um número válido: {payload_str}")
                        return
                else:
                    # For other topics, if it's not JSON, it's an error
                    print(f"❌ Erro: Payload para o tópico {message.topic} não é um JSON válido: {payload_str}")
                    return

            # If json.loads successfully parsed a non-dict (e.g., a simple number),
            # we need to ensure 'payload' is a dict for consistent .get() calls.
            if not isinstance(parsed_payload, dict):
                if message.topic == 'sensor/umidade':
                    # This specific handling is for when json.loads('32.00') directly results in 32.0 (float)
                    try:
                        valor_umidade = float(payload_str)
                        parsed_payload = {
                            'id_device': 'unknown_sensor_id',
                            'valor_umidade': valor_umidade,
                            'status_umidade': 'OK'
                        }
                    except ValueError:
                        print(f"❌ Erro: Payload para sensor/umidade não é um número válido após decodificação JSON: {payload_str}")
                        return
                else:
                    # For other topics, if it's not a dict, it's an unexpected format
                    print(f"❌ Erro: Payload inesperado para o tópico {message.topic}. Esperado JSON (dicionário), mas recebeu: {type(parsed_payload).__name__}. Payload: {payload_str}")
                    return

            # Now, parsed_payload is guaranteed to be a dictionary (either from valid JSON or fabricated)
            payload = parsed_payload # Use 'payload' for consistency with existing code logic

            # --- Unified Timestamp Parsing Logic ---
            # Default to the current time if no valid timestamp is found
            data_hora = datetime.datetime.now()
            timestamp_value = payload.get('timestamp')

            if timestamp_value is not None:
                try:
                    # First, try to parse as Unix timestamp (milliseconds)
                    timestamp_int = int(timestamp_value)
                    # Convert milliseconds to seconds before creating datetime object
                    data_hora = datetime.datetime.fromtimestamp(timestamp_int / 1000)
                except ValueError:
                    # If it's not an integer, try to parse as a string datetime
                    try:
                        # Assuming a common format, adjust if yours is different
                        data_hora = datetime.datetime.strptime(str(timestamp_value), "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        # Fallback if string parsing also fails
                        print(f"⚠️ Não foi possível analisar o timestamp '{timestamp_value}' no tópico '{message.topic}'. Usando a hora atual.")
            # --- End Unified Timestamp Parsing Logic ---

            nova_leitura = None # Initialize nova_leitura outside conditional blocks

            if message.topic == 'balanca/leitura':
                # Extract data for BalancaLeituras, using .get() for safe access
                id_device = payload.get('id_device')
                peso = payload.get('peso')

                if id_device is not None and peso is not None:
                    nova_leitura = BalancaLeituras(
                        id_device=id_device,
                        peso=peso,
                        peso_datetime=data_hora
                    )
                else:
                    # Log if critical data is missing for balanca/leitura
                    print(f"⚠️ Payload inválido ou incompleto para balanca/leitura: 'id_device' ou 'peso' ausente. Payload: {payload_str}")
                    return # Exit function if data is invalid

            elif message.topic == 'motor/status':
                # Extract data for MotorLeituras
                # Assuming 'clientId' from the MQTT payload maps to 'id_device' in your model
                id_device = payload.get('clientId')
                # Assuming 'status' from the MQTT payload maps to 'status_motor' in your model
                status_motor = payload.get('status')

                if id_device is not None and status_motor is not None:
                    nova_leitura = MotorLeituras(
                        id_device=id_device,
                        status_motor=status_motor,
                        motor_datetime=data_hora
                    )
                else:
                    # Log if critical data is missing for motor/status
                    print(f"⚠️ Payload inválido ou incompleto para motor/status: 'clientId' ou 'status' ausente. Payload: {payload_str}")
                    return # Exit function if data is invalid

            elif message.topic == 'sensor/umidade':
                # Extract data for SensorLeituras - now using the potentially fabricated 'payload' dictionary
                id_device = payload.get('id_device')
                valor_umidade = payload.get('valor_umidade')
                status_umidade = payload.get('status_umidade')

                if id_device is not None and valor_umidade is not None and status_umidade is not None:
                    nova_leitura = SensorLeituras(
                        id_device=id_device,
                        valor_umidade=valor_umidade,
                        status_umidade=status_umidade,
                        sensor_datetime=data_hora
                    )
                else:
                    # Log if critical data is missing for sensor/umidade even after payload processing
                    print(f"⚠️ Payload inválido ou incompleto para sensor/umidade: 'id_device', 'valor_umidade' ou 'status_umidade' ausente. Payload: {payload_str}")
                    return # Exit function if data is invalid

            else:
                # Log if the topic is not recognized or handled
                print(f"⚠️ Tópico não tratado: {message.topic}")
                return # Exit function for unhandled topics

            # Save the new reading to the database if it was successfully created
            if nova_leitura:
                with app.app_context(): # Ensure database operations are within an app context
                    db.session.add(nova_leitura)
                    db.session.commit()
                    print(f"✅ Leitura salva no banco de dados do tópico: {message.topic}")

        except Exception as e:
            # Catch any other unexpected errors during message processing
            print(f"❌ Erro geral ao processar mensagem MQTT: {e}. Tópico: {message.topic}, Payload: {message.payload.decode('utf-8')}")

    # API Route to Send Commands to Motor
    @app.route('/api/enviar_comando_motor', methods=['POST'])
    def enviar_comando_motor():
        """
        API endpoint to send commands to a motor via MQTT.
        Expects a JSON payload with 'id_device' and 'comando'.
        """
        data = request.get_json()
        device_id = data.get('id_device')
        comando = data.get('comando')

        if not device_id or not comando:
            return jsonify({"status": "erro", "mensagem": "ID do dispositivo e comando são obrigatórios."}), 400

        try:
            with app.app_context():
                # Query the database for motor information based on device_id
                motor_info = Motor.query.filter_by(id_device=device_id).first()
                if motor_info:
                    # Construct the command topic using information from the database
                    topico_comando = f"{motor_info.topico_motor}/comando"
                    
                    # Create the JSON payload for the MQTT command
                    payload = json.dumps({
                        "id_device": device_id,
                        "comando": comando,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

                    # Publish the command to the MQTT broker
                    mqtt_client.publish(topico_comando, payload)
                    print(f"⬆️ Comando '{comando}' enviado para o motor ID {device_id} no tópico {topico_comando}")
                    return jsonify({"status": "sucesso", "mensagem": "Comando enviado!"}), 200
                else:
                    # Return error if motor with specified ID is not found
                    return jsonify({"status": "erro", "mensagem": f"Motor com ID {device_id} não encontrado."}), 404
        except Exception as e:
            # Handle any exceptions during the command sending process
            print(f"❌ Erro ao enviar comando MQTT: {e}")
            return jsonify({"status": "erro", "mensagem": f"Erro interno ao enviar comando: {e}"}), 500
        
    @app.route('/')
    def index():
        """
        Renders the login HTML page as the application's root.
        """
        return redirect(url_for('user_blueprint.login'))

    return app

