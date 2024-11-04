from flask import Flask, jsonify
import subprocess
import os
import sys
import tempfile

app = Flask(__name__)

@app.route('/start_app', methods=['GET'])
def start_app():
    try:
        # Caminho para o seu script Python
        app_path = './agent.py'  # Substitua pelo caminho correto

        # Use subprocess para iniciar a aplicação e capturar a saída
        result = subprocess.run(['python', app_path], capture_output=True, text=True)

        # Verifica se houve erro na execução do script
        if result.returncode != 0:
            return jsonify({"error": result.stderr.strip()}), 500

        # Se não houver erro, pega a saída padrão do script
        files_output = result.stdout.strip()

        # Converte a saída em uma lista (pode ser ajustada conforme necessidade)
        if files_output:
            files = files_output.splitlines()
            return jsonify({"files": files}), 200
        else:
            return jsonify({"error": "Nenhum arquivo encontrado ou caminho inválido."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
