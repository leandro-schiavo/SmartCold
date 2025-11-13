from .sensor import Sensor
import random

class SensorTemperatura(Sensor):
    def __init__(self, nome="Sensor de Temperatura"):
        super().__init__(nome, unidade="°C")
        self._min = -5.0
        self._max = 50.0
        
    def ler_dados(self):
        # Simula leitura real com variação natural
        temperatura_base = 22.0
        variacao = random.uniform(-3, 3)
        ruido = random.uniform(-0.5, 0.5)
        return round(temperatura_base + variacao + ruido, 1)
        
    def definir_limites(self, min_temp, max_temp):
        self._min = min_temp
        self._max = max_temp
        
    def verificar_alerta(self):
        if self._valor is None:
            return False
        return self._valor < self._min or self._valor > self._max