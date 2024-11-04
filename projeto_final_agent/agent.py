from flask import Flask, jsonify, request
import os
from tkinter import Tk, filedialog
from flask_cors import CORS
import requests
from threading import Thread

app = Flask(__name__)
CORS(app)

@app.route('/get_images', methods=['POST'])
def get_images():
    # Obtem o caminho da pasta a partir do corpo da requisição
    folder_path = request.json.get('folder_path')

    if folder_path and os.path.isdir(folder_path):
        # Listar arquivos na pasta selecionada e criar uma lista com o caminho completo
        files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
        return jsonify(files), 200
    else:
        return jsonify({"error": "Caminho inválido ou nenhuma pasta selecionada."}), 400

def select_folder():
    # Inicia a interface gráfica para seleção de pastas
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    folder_path = filedialog.askdirectory()  # Abre o diálogo para escolher uma pasta
    return folder_path

def main():
    folder_path = select_folder()  # Permite que o usuário escolha uma pasta
    if folder_path:  # Se uma pasta foi selecionada
        # Faz uma requisição para o servidor Flask
        response = requests.post('http://127.0.0.1:5000/get_images', json={"folder_path": folder_path})
        try:
            response.raise_for_status()  # Lança um erro para códigos de status HTTP 4xx/5xx
            files = response.json()  # Tenta decodificar a resposta JSON
            print("Arquivos encontrados:", files)
        except requests.exceptions.HTTPError as errh:
            print("Erro HTTP:", errh)
        except requests.exceptions.RequestException as err:
            print("Erro na requisição:", err)
        except ValueError as json_err:
            print("Erro ao decodificar JSON:", json_err)
    else:
        print("Nenhuma pasta selecionada.")

if __name__ == '__main__':
    # Inicia o servidor Flask em uma thread separada
    flask_thread = Thread(target=lambda: app.run(debug=True, use_reloader=False))
    flask_thread.start()
    main()
