from flask import Flask, render_template, jsonify, Response
from flask_cors import CORS
from sensors.temperatura_sensor import SensorTemperatura
from sensors.porta_sensor import SensorPorta
from sistema.gerenciador_sensores import GerenciadorSensores
from sistema.historico import HistoricoDados
from sistema.alerta_manager import AlertaManager
import json
import time
import threading

app = Flask(__name__)
CORS(app)

# Instâncias globais
gerenciador = GerenciadorSensores()
historico = HistoricoDados(max_registros=50)
alerta_manager = AlertaManager()

def inicializar_sistema():
    """Inicializa os sensores"""
    sensor_temp = SensorTemperatura()
    sensor_porta = SensorPorta()
    
    gerenciador.registrar_sensor(sensor_temp)
    gerenciador.registrar_sensor(sensor_porta)
    gerenciador.registrar_callback(processar_leitura)
    
def processar_leitura(sensor_nome, valor):
    """Processa leituras dos sensores"""
    historico.adicionar_leitura(sensor_nome, valor)
    
    # Verifica alertas
    if "Temperatura" in sensor_nome:
        sensor = gerenciador.sensores[sensor_nome]
        if sensor.verificar_alerta():
            mensagem = f"🌡️ Temperatura fora do limite: {valor}°C"
            alerta_manager.gerar_alerta(mensagem, "HIGH")
            
    elif "Porta" in sensor_nome:
        sensor = gerenciador.sensores[sensor_nome]
        if sensor.detectar_mudanca() and valor == "ABERTA":
            alerta_manager.gerar_alerta("🚪 ALERTA DE SEGURANÇA: Porta foi aberta!", "HIGH")

# Rotas da API
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Retorna status atual dos sensores"""
    return jsonify({
        "temperatura": gerenciador.obter_estado("Sensor de Temperatura"),
        "porta": gerenciador.obter_estado("Sensor de Porta"),
        "alertas": alerta_manager.get_alertas(),
        "grafico": historico.gerar_grafico_base64()
    })

@app.route('/stream')
def stream():
    """SSE - Server Sent Events para atualizações em tempo real"""
    def event_stream():
        while True:
            data = {
                "temperatura": gerenciador.obter_estado("Sensor de Temperatura"),
                "porta": gerenciador.obter_estado("Sensor de Porta"),
                "alertas": alerta_manager.get_alertas(),
                "grafico": historico.gerar_grafico_base64()
            }
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(2)  # Atualiza a cada 2 segundos
    
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/api/exportar')
def exportar():
    """Exporta dados"""
    historico.exportar_json()
    alerta_manager.gerar_alerta("📁 Dados exportados para 'historico_dados.json'", "LOW")
    return jsonify({"sucesso": True})

# Inicialização
if __name__ == '__main__':
    inicializar_sistema()
    gerenciador.iniciar_todos()
    app.run(debug=True, threaded=True)