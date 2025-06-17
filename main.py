from machine import Pin, PWM, freq
from hx711 import HX711
import time
import dht
import network
import utime
import umqtt.simple as mqtt
import ujson

# ==== CONFIGURAÇÕES WIFI ====
SSID = 'Wokwi-GUEST'
PASSWORD = ''

# ==== CONFIGURAÇÕES MQTT ====
BROKER = 'mqtt-dashboard.com'
TOPICO_UMIDADE = 'sensor/umidade'

# ==== CONEXÃO WIFI ====
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("conectando ao wi-fi...", end='')
while not wifi.isconnected():
    print('.', end='')
    time.sleep(1)
print('\nconectado! ip:', wifi.ifconfig()[0])

# ==== CLIENTE MQTT ====
client_id = 'esp32_sensor_01'
mqtt_client = mqtt.MQTTClient(client_id, BROKER)
mqtt_client.connect()
print('mqtt conectado ao broker.')

# ==== HX711 (balança) ====
hx = HX711(d_out=4, pd_sck=14)
hx.channel = HX711.CHANNEL_A_128
freq(160000000)

offset = 0
scale = 1.0

# ==== SERVO (GPIO 26) ====
servo = PWM(Pin(26), freq=50)
servo_aberto = False

# ==== DHT11 (GPIO 25) ====
sensor_dht = dht.DHT11(Pin(25))

# ==== FUNÇÕES ====
def abrir_servo():
    global servo_aberto
    servo.duty(40)
    servo_aberto = True
    print("servo aberto")

def fechar_servo():
    global servo_aberto
    servo.duty(115)
    servo_aberto = False
    print("servo fechado")

def tare(times=10):
    global offset
    offset = sum(hx.read() for _ in range(times)) / times
    print(f"offset: {offset}")

def calibrar(peso_conhecido, times=100):
    global scale
    input(f"coloque {peso_conhecido}g e pressione enter...")
    leitura = sum(hx.read() for _ in range(times)) / times
    scale = (leitura - offset) / peso_conhecido
    print(f"fator de escala: {scale}")

def ler_peso(times=5):
    leitura = sum(hx.read() for _ in range(times)) / times
    return max(0, (leitura - offset) / scale)

def ler_umidade():
    try:
        sensor_dht.measure()
        umidade = sensor_dht.humidity()
        print(f"umidade: {umidade}%")
        return umidade
    except Exception as e:
        print("erro dht:", e)
        return None

def publish_mqtt_umidade():
    umidade = ler_umidade()
    if umidade is not None:
        status = 'Bom'
        if umidade < 30:
            status = 'Baixa'
        elif umidade > 70:
            status = 'Alta'
        
        payload = ujson.dumps({
            "id_device": client_id,
            "valor_umidade": umidade,
            "status_umidade": status,
            "timestamp": int(utime.time() * 1000)
        })
        mqtt_client.publish(TOPICO_UMIDADE, payload)
        print("umidade enviada via mqtt")

# ==== INÍCIO ====
print("=== calibração ===")
tare(65)
calibrar(380)

print("=== monitorando ===")
input("pressione enter para abrir o servo...")
abrir_servo()

# controle de tempo para enviar a cada 5 minutos (300s)
last_umidade_time = utime.time()

while True:
    try:
        peso = ler_peso()
        print(f"peso: {peso:.1f}g")

        if servo_aberto and peso >= 700:
            fechar_servo()

        # envia a cada 5 min
        now = utime.time()
        if now - last_umidade_time >= 300:
            publish_mqtt_umidade()
            last_umidade_time = now

        time.sleep(5)

    except Exception as e:
        print("erro:", e)