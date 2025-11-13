from abc import ABC, abstractmethod
from datetime import datetime
import random
import time
from threading import Thread

class Sensor(ABC):
    def __init__(self, nome, unidade=""):
        self.nome = nome
        self.unidade = unidade
        self._valor = None
        self._ativo = False
        self._observadores = []
        
    @abstractmethod
    def ler_dados(self):
        pass
    
    def adicionar_observador(self, callback):
        self._observadores.append(callback)
        
    def notificar_observadores(self):
        for callback in self._observadores:
            callback(self.nome, self._valor)
            
    def iniciar_monitoramento(self, intervalo=2):
        self._ativo = True
        Thread(target=self._monitorar, args=(intervalo,), daemon=True).start()
        
    def parar_monitoramento(self):
        self._ativo = False
        
    def _monitorar(self, intervalo):
        while self._ativo:
            try:
                self._valor = self.ler_dados()
                self.notificar_observadores()
            except Exception as e:
                print(f"Erro no sensor {self.nome}: {e}")
            time.sleep(intervalo)
            
    @property
    def valor(self):
        return self._valor