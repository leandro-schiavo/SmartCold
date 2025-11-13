import json
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

class HistoricoDados:
    def __init__(self, max_registros=100):
        self.max_registros = max_registros
        self.dados = {
            "temperatura": [],
            "porta": [],
            "timestamps": []
        }
        
    def adicionar_leitura(self, sensor_nome, valor):
        timestamp = datetime.now()
        
        if "Temperatura" in sensor_nome:
            self.dados["temperatura"].append({
                "valor": valor,
                "hora": timestamp.strftime("%H:%M:%S")
            })
        elif "Porta" in sensor_nome:
            self.dados["porta"].append({
                "valor": valor,
                "hora": timestamp.strftime("%H:%M:%S")
            })
            
        self.dados["timestamps"].append(timestamp)
        
        # Mantém apenas os últimos registros
        if len(self.dados["temperatura"]) > self.max_registros:
            self.dados["temperatura"].pop(0)
        if len(self.dados["porta"]) > self.max_registros:
            self.dados["porta"].pop(0)
        if len(self.dados["timestamps"]) > self.max_registros:
            self.dados["timestamps"].pop(0)
            
    def exportar_json(self):
        with open("historico_dados.json", "w") as f:
            json.dump(self.dados, f, indent=4, default=str)
            
    def gerar_grafico_base64(self):
        """Gera gráfico em base64 para web"""
        if not self.dados["temperatura"]:
            return None
            
        fig, ax = plt.subplots(figsize=(10, 4), dpi=80)
        valores = [r["valor"] for r in self.dados["temperatura"]]
        horas = [r["hora"] for r in self.dados["temperatura"]]
        
        ax.plot(horas, valores, marker='o', linewidth=2, color='#2E86AB')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_xlabel('Hora')
        ax.set_title('Histórico de Temperatura')
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Converte para PNG em base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"