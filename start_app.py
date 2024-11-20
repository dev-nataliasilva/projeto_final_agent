import os
import sys
import winreg
from pystray import Icon, Menu, MenuItem
from PIL import Image
from flask import Flask, jsonify
import subprocess
import json
from flask_cors import CORS
import logging
import threading
import time
import psutil

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask App
app = Flask(__name__)
CORS(app)

@app.route('/start_app', methods=['GET'])
def start_app():
    try:
        # Caminho para o seu script Python
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        app_path = os.path.join(base_dir, 'agent.py')
        logging.info(f'Iniciando o subprocesso com o script: {app_path}')

        # Use subprocess para iniciar a aplicação e capturar a saída
        result = subprocess.run(['python', app_path], capture_output=True, text=True)

        if result.returncode != 0:
            logging.error(f'Erro ao executar o script agent.py: {result.stderr.strip()}')
            return jsonify({"error": result.stderr.strip()}), 500

        files_output = result.stdout.strip()
        if files_output:
            try:
                files = json.loads(files_output)
                logging.info(f'Arquivos encontrados: {files}')
                return jsonify(files), 200
            except json.JSONDecodeError:
                logging.error('A saída não é um JSON válido.')
                return jsonify({"error": "A saída não é um JSON válido."}), 400
        else:
            logging.warning('Nenhum arquivo encontrado ou caminho inválido.')
            return jsonify({"error": "Nenhum arquivo encontrado ou caminho inválido."}), 400

    except Exception as e:
        logging.error(f'Erro inesperado: {str(e)}')
        return jsonify({"error": str(e)}), 500

def add_to_startup():
    """Adiciona o executável à inicialização do Windows."""
    exe_path = sys.executable  # Caminho do executável Python (ou do executável compilado)
    key = winreg.HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    reg_key = "Agente-OndeSalvei"  # Nome para identificar seu aplicativo no registro

    try:
        # Abre a chave de registro de inicialização
        with winreg.OpenKey(key, reg_path, 0, winreg.KEY_WRITE) as reg:
            # Adiciona o caminho do executável à chave de inicialização
            winreg.SetValueEx(reg, reg_key, 0, winreg.REG_SZ, exe_path)
        logging.info("Aplicação adicionada à inicialização do Windows.")
    except Exception as e:
        logging.error(f"Erro ao adicionar ao registro de inicialização: {str(e)}")

def run_flask():
    """Executa o servidor Flask em uma thread separada."""
    logging.info('Iniciando o servidor Flask...')
    app.run(debug=False, use_reloader=False)  # Desativa o reloader para não reiniciar o servidor

def on_quit(icon, item):
    """Encerra a aplicação, incluindo Flask e o ícone do System Tray."""
    logging.info('Iniciando o processo de encerramento da aplicação...')
    
    # Encerra o processo do Flask
    for proc in psutil.process_iter(['pid', 'name']):
        if 'flask' in proc.info['name'].lower() or 'python' in proc.info['name'].lower():
            logging.info(f"Encerrando processo: {proc.info['pid']} - {proc.info['name']}")
            proc.terminate()
            proc.wait()

    # Encerra o ícone do System Tray
    logging.info("Encerrando o ícone do System Tray...")
    icon.stop()

    # Encerra o programa
    logging.info('Aplicação encerrada com sucesso.')
    sys.exit(0)

def main():
    # Adiciona o executável à inicialização
    logging.info('Adicionando a aplicação à inicialização do Windows...')
    add_to_startup()

    # Cria e exibe o ícone no System Tray
    logging.info('Configurando o menu do System Tray...')
    menu = Menu(
        MenuItem('Está ativo!', lambda: logging.info("A aplicação está ativa.")),  # Exibe uma opção com o texto "Está ativo!"
        MenuItem('Sair', on_quit)  # Continua com a opção "Sair"
    )

    # Carrega a imagem do ícone a partir do arquivo .ico
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_dir, 'images/Onde-salvei-lemure-preto.ico')
    image = Image.open(icon_path)

    # Configura o ícone no System Tray
    logging.info('Carregando o ícone no System Tray...')
    icon = Icon("Agente - Onde Salvei", image, menu=menu)
    icon.title = "Agente - Onde Salvei?"

    # Cria uma thread para rodar o Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Exibe o ícone no System Tray
    logging.info('Exibindo o ícone no System Tray...')
    icon.run()

if __name__ == "__main__":
    logging.info('Iniciando a aplicação...')
    main()