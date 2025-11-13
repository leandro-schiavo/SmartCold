from .sensor import Sensor

class SensorPorta(Sensor):
    def __init__(self, nome="Sensor de Porta"):
        super().__init__(nome, unidade="")
        self._estado_anterior = None
        
    def ler_dados(self):
        # Simula abertura/fechamento (70% chance de fechada)
        import random
        return "ABERTA" if random.random() < 0.3 else "FECHADA"
        
    def detectar_mudanca(self):
        if self._estado_anterior is None:
            self._estado_anterior = self._valor
            return False
        mudou = self._estado_anterior != self._valor
        self._estado_anterior = self._valor
        return mudou