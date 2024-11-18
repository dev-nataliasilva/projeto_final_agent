import os
import sys
import threading
import winreg  # Para manipulação do registro do Windows
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from flask import Flask, jsonify
import subprocess
import json
from flask_cors import CORS
from werkzeug.serving import make_server

# Flask App
app = Flask(__name__)
CORS(app)

@app.route('/start_app', methods=['GET'])
def start_app():
    try:
        # Caminho para o seu script Python
        app_path = './agent.py'  # Substitua pelo caminho correto

        # Use subprocess para iniciar a aplicação e capturar a saída
        result = subprocess.run(['python', app_path], capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": result.stderr.strip()}), 500

        files_output = result.stdout.strip()
        if files_output:
            try:
                files = json.loads(files_output)
                return jsonify(files), 200
            except json.JSONDecodeError:
                return jsonify({"error": "A saída não é um JSON válido."}), 400
        else:
            return jsonify({"error": "Nenhum arquivo encontrado ou caminho inválido."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Função para criar o ícone do System Tray
def on_quit(icon, item):
    """Encerra o ícone e o servidor Flask."""
    # Parar o servidor Flask
    global flask_server
    if flask_server:
        flask_server.shutdown()

    icon.stop()  # Encerra o ícone no System Tray
    sys.exit(0)  # Encerra o programa


def run_flask():
    """Executa o servidor Flask em uma thread separada."""
    global flask_server
    flask_server = make_server('0.0.0.0', 5000, app)
    flask_server.serve_forever()


def add_to_startup():
    """Adiciona o executável à inicialização do Windows."""
    exe_path = sys.executable  # Caminho do executável Python (ou do executável compilado)
    key = winreg.HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    reg_key = "MyApp"  # Nome para identificar seu aplicativo no registro

    try:
        # Abre a chave de registro de inicialização
        with winreg.OpenKey(key, reg_path, 0, winreg.KEY_WRITE) as reg:
            # Adiciona o caminho do executável à chave de inicialização
            winreg.SetValueEx(reg, reg_key, 0, winreg.REG_SZ, exe_path)
            print("Aplicação adicionada à inicialização do Windows.")
    except Exception as e:
        print(f"Erro ao adicionar ao registro: {str(e)}")


def main():
    global flask_server

    # Adiciona o executável à inicialização
    add_to_startup()

    # Executa o Flask em uma thread separada
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Configura o menu do System Tray
    menu = Menu(
        MenuItem('Está ativo!', lambda: print("A aplicação está ativa.")),  # Exibe uma opção com o texto "Está ativo!"
        MenuItem('Sair', on_quit)  # Continua com a opção "Sair"
    )

    # Carrega a imagem do ícone a partir do arquivo .ico
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_dir, 'images/Onde-salvei-lemure-preto.ico')
    image = Image.open(icon_path)

    # Configura o ícone no System Tray
    icon = Icon("MyApp", image, menu=menu)
    icon.title = "Agente - Onde Salvei?"
    icon.run()  # Mostra o ícone no System Tray


if __name__ == "__main__":
    main()
