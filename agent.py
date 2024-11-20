import os
import json  # Importar a biblioteca json
from tkinter import Tk, filedialog
from PIL import Image
import numpy as np

def select_folder():
    # Inicia a interface gráfica para seleção de pastas
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    folder_path = filedialog.askdirectory()  # Abre o diálogo para escolher uma pasta
    return folder_path

def is_image_file(filename):
    # Verifica se o arquivo é uma imagem com base na extensão
    image_extensions = ('.jpg', '.jpeg', '.png')
    return filename.lower().endswith(image_extensions)

def calculate_average_rgb(image_path):
    # Abre a imagem e calcula a média RGB
    with Image.open(image_path) as img:
        img = img.convert('RGB')  # Garante que a imagem está no formato RGB
        np_img = np.array(img)  # Converte a imagem para um array NumPy
        avg_color = np.mean(np_img, axis=(0, 1))  # Calcula a média RGB
        return [int(value) for value in avg_color]  # Converte cada valor para int

def list_files_recursively(folder_path):
    # Lista todos os arquivos de imagem em uma pasta e suas subpastas
    files_info = []  # Usado para armazenar informações de cada arquivo
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if is_image_file(file):  # Filtra apenas arquivos de imagem
                file_path = os.path.join(root, file)  # Caminho completo do arquivo
                avg_rgb = calculate_average_rgb(file_path)  # Calcula a média RGB
                files_info.append({
                    'path': file_path,
                    'average_rgb': avg_rgb  # Adiciona a média RGB ao dicionário
                })
    return files_info  # Retorna a lista de informações dos arquivos

def list_files():
    folder_path = select_folder()  # Permite que o usuário escolha uma pasta
    if folder_path and os.path.isdir(folder_path):  # Se uma pasta foi selecionada e é válida
        # Listar arquivos de imagem na pasta selecionada recursivamente
        files = list_files_recursively(folder_path)
        return files  # Retorna a lista de arquivos e suas médias RGB
    else:
        return []  # Retorna uma lista vazia se a pasta for inválida

if __name__ == '__main__':
    files = list_files()  # Para testes locais, você pode chamar diretamente
    print(json.dumps(files))  # Imprime a lista como JSON
