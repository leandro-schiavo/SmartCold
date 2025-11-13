// Conecta ao SSE para atualizações em tempo real
const eventSource = new EventSource('/stream');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    atualizarDashboard(data);
};

function atualizarDashboard(data) {
    // Atualiza Temperatura
    const temp = data.temperatura;
    const tempValor = document.getElementById('temp-valor');
    const tempStatus = document.getElementById('temp-status');
    
    if (temp !== null) {
        tempValor.textContent = temp;
        if (temp < 18) {
            tempValor.className = 'text-6xl font-bold text-blue-400';
            tempStatus.textContent = '❄️ Status: FRIO';
            tempStatus.className = 'mt-4 text-sm text-blue-400';
        } else if (temp > 26) {
            tempValor.className = 'text-6xl font-bold text-red-400';
            tempStatus.textContent = '🔥 Status: QUENTE';
            tempStatus.className = 'mt-4 text-sm text-red-400';
        } else {
            tempValor.className = 'text-6xl font-bold text-green-400';
            tempStatus.textContent = '✅ Status: NOMINAL';
            tempStatus.className = 'mt-4 text-sm text-green-400';
        }
    }

    // Atualiza Porta
    const porta = data.porta;
    const portaValor = document.getElementById('porta-valor');
    const portaStatus = document.getElementById('porta-status');
    
    if (porta !== null) {
        portaValor.textContent = porta;
        if (porta === 'ABERTA') {
            portaValor.className = 'text-6xl font-bold text-orange-400';
            portaStatus.textContent = '⚠️ Status: VULNERÁVEL';
            portaStatus.className = 'mt-4 text-sm text-orange-400';
        } else {
            portaValor.className = 'text-6xl font-bold text-green-400';
            portaStatus.textContent = '🔒 Status: SEGURA';
            portaStatus.className = 'mt-4 text-sm text-green-400';
        }
    }

    // Atualiza Alertas
    const alertasContainer = document.getElementById('alertas-container');
    alertasContainer.innerHTML = '';
    
    if (data.alertas && data.alertas.length > 0) {
        data.alertas.slice().reverse().forEach(alerta => {
            const div = document.createElement('div');
            div.className = `p-3 rounded-lg text-white font-bold ${alerta.cor} shadow-lg`;
            div.innerHTML = `<i class="fas fa-exclamation-triangle mr-2"></i>${alerta.hora} - ${alerta.mensagem}`;
            alertasContainer.appendChild(div);
        });
    }

    // Atualiza Gráfico
    const graficoContainer = document.getElementById('grafico-container');
    if (data.grafico) {
        graficoContainer.innerHTML = `<img src="${data.grafico}" class="max-w-full h-auto rounded-lg shadow-lg">`;
    }
}

function exportarDados() {
    fetch('/api/exportar')
        .then(response => response.json())
        .then(data => {
            alert('Dados exportados com sucesso!');
        });
}