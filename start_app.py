import os
import sys
import winreg  # Para manipular o registro do Windows
from pystray import Icon, Menu, MenuItem  # Para criar um ícone no System Tray
from PIL import Image  # Para carregar a imagem do ícone
from flask import Flask, jsonify  # Para criar o servidor Flask
import subprocess  # Para rodar subprocessos (executar scripts)
import json  # Para manipulação de JSON
from flask_cors import CORS  # Para habilitar CORS no Flask
import logging  # Para logging de informações
import threading  # Para rodar o Flask em uma thread separada
import time  # Para manipulação de tempo
import psutil  # Para gerenciar processos (encerrar o Flask)

# Configuração de logging para capturar informações sobre o funcionamento do programa
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask App
app = Flask(__name__)  # Criação da aplicação Flask
CORS(app)  # Habilita CORS para permitir requisições de diferentes origens

@app.route('/start_app', methods=['GET'])
def start_app():
    try:
        # Caminho para o seu script Python (agent.py)
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        app_path = os.path.join(base_dir, 'agent.py')
        logging.info(f'Iniciando o subprocesso com o script: {app_path}')

        # Usando subprocess para rodar o script Python e capturar a saída
        result = subprocess.run(['python', app_path], capture_output=True, text=True)

        if result.returncode != 0:
            # Caso o subprocesso retorne um erro, loga e retorna uma resposta de erro
            logging.error(f'Erro ao executar o script agent.py: {result.stderr.strip()}')
            return jsonify({"error": result.stderr.strip()}), 500

        files_output = result.stdout.strip()  # Captura a saída do script agent.py
        if files_output:
            try:
                # Tenta converter a saída para JSON (espera-se que seja uma lista de arquivos)
                files = json.loads(files_output)
                logging.info(f'Arquivos encontrados: {files}')
                return jsonify(files), 200  # Retorna os arquivos encontrados como JSON
            except json.JSONDecodeError:
                # Caso a saída não seja um JSON válido, retorna um erro
                logging.error('A saída não é um JSON válido.')
                return jsonify({"error": "A saída não é um JSON válido."}), 400
        else:
            logging.warning('Nenhum arquivo encontrado ou caminho inválido.')
            return jsonify({"error": "Nenhum arquivo encontrado ou caminho inválido."}), 400

    except Exception as e:
        # Caso haja algum erro inesperado, retorna o erro
        logging.error(f'Erro inesperado: {str(e)}')
        return jsonify({"error": str(e)}), 500

def add_to_startup():
    """Adiciona o executável à inicialização do Windows."""
    exe_path = sys.executable  # Obtém o caminho do executável Python
    key = winreg.HKEY_CURRENT_USER  # A chave de registro para o usuário atual
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"  # Caminho para a chave de inicialização
    reg_key = "Agente-OndeSalvei"  # Nome que será usado para identificar o aplicativo

    try:
        # Abre a chave de registro e adiciona o caminho do executável para iniciar automaticamente
        with winreg.OpenKey(key, reg_path, 0, winreg.KEY_WRITE) as reg:
            winreg.SetValueEx(reg, reg_key, 0, winreg.REG_SZ, exe_path)
        logging.info("Aplicação adicionada à inicialização do Windows.")
    except Exception as e:
        logging.error(f"Erro ao adicionar ao registro de inicialização: {str(e)}")

def run_flask():
    """Executa o servidor Flask em uma thread separada."""
    logging.info('Iniciando o servidor Flask...')
    app.run(debug=False, use_reloader=False)  # Desativa o reloader para não reiniciar o servidor

def on_quit(icon, item):
    """Função que é chamada ao clicar em 'Sair' no menu do ícone do System Tray."""
    logging.info('Iniciando o processo de encerramento da aplicação...')
    
    # Encerra o processo do Flask
    for proc in psutil.process_iter(['pid', 'name']):
        if 'flask' in proc.info['name'].lower() or 'python' in proc.info['name'].lower():
            logging.info(f"Encerrando processo: {proc.info['pid']} - {proc.info['name']}")
            proc.terminate()  # Termina o processo do Flask
            proc.wait()  # Aguarda o término do processo

    # Encerra o ícone do System Tray
    logging.info("Encerrando o ícone do System Tray...")
    icon.stop()

    # Finaliza o programa
    logging.info('Aplicação encerrada com sucesso.')
    sys.exit(0)

def main():
    # Adiciona o executável à inicialização do Windows
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