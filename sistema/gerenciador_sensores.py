from typing import Dict, List, Callable

class GerenciadorSensores:
    def __init__(self):
        self.sensores: Dict[str, object] = {}
        self.callbacks: List[Callable] = []
        
    def registrar_sensor(self, sensor):
        self.sensores[sensor.nome] = sensor
        sensor.adicionar_observador(self._notificacao_central)
        
    def registrar_callback(self, callback):
        self.callbacks.append(callback)
        
    def _notificacao_central(self, sensor_nome, valor):
        for callback in self.callbacks:
            callback(sensor_nome, valor)
            
    def iniciar_todos(self):
        for sensor in self.sensores.values():
            sensor.iniciar_monitoramento()
            
    def parar_todos(self):
        for sensor in self.sensores.values():
            sensor.parar_monitoramento()
            
    def obter_estado(self, nome_sensor):
        sensor = self.sensores.get(nome_sensor)
        return sensor.valor if sensor else None