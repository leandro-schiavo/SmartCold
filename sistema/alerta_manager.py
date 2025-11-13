from datetime import datetime

class AlertaManager:
    def __init__(self):
        self.historico_alertas = []
        
    def gerar_alerta(self, mensagem, nivel="MEDIUM"):
        alerta = {
            "hora": datetime.now().strftime("%H:%M:%S"),
            "mensagem": mensagem,
            "nivel": nivel,
            "cor": self._get_cor(nivel)
        }
        self.historico_alertas.append(alerta)
        
        # Mantém apenas os últimos 10 alertas
        if len(self.historico_alertas) > 10:
            self.historico_alertas.pop(0)
            
        return alerta
        
    def _get_cor(self, nivel):
        cores = {
            "LOW": "bg-green-500",
            "MEDIUM": "bg-orange-500", 
            "HIGH": "bg-red-500"
        }
        return cores.get(nivel, "bg-orange-500")
        
    def get_alertas(self):
        return self.historico_alertas