import os
import json  # Importa a biblioteca json para manipulação de dados no formato JSON
from tkinter import Tk, filedialog  # Importa a interface gráfica para seleção de pastas
from PIL import Image  # Importa a biblioteca Pillow para manipulação de imagens
import numpy as np  # Importa o NumPy para cálculos eficientes em arrays

def select_folder():
    # Inicia a interface gráfica para seleção de pastas
    root = Tk()  # Cria uma instância da janela principal
    root.withdraw()  # Esconde a janela principal (não queremos mostrar a interface)
    folder_path = filedialog.askdirectory()  # Abre o diálogo para o usuário escolher uma pasta
    return folder_path  # Retorna o caminho da pasta escolhida

def is_image_file(filename):
    # Verifica se o arquivo é uma imagem com base na extensão do nome do arquivo
    image_extensions = ('.jpg', '.jpeg', '.png')  # Extensões válidas para imagens
    return filename.lower().endswith(image_extensions)  # Retorna True se a extensão for uma das válidas

def calculate_average_rgb(image_path):
    # Abre a imagem e calcula a média das cores RGB
    with Image.open(image_path) as img:  # Abre a imagem usando Pillow
        img = img.convert('RGB')  # Converte a imagem para o formato RGB (caso não esteja)
        np_img = np.array(img)  # Converte a imagem para um array NumPy para facilitar os cálculos
        avg_color = np.mean(np_img, axis=(0, 1))  # Calcula a média dos valores de RGB em toda a imagem
        return [int(value) for value in avg_color]  # Retorna a média de cada canal de cor como um inteiro

def list_files_recursively(folder_path):
    # Lista todos os arquivos de imagem em uma pasta e suas subpastas
    files_info = []  # Lista para armazenar informações dos arquivos de imagem encontrados
    for root, dirs, files in os.walk(folder_path):  # Itera sobre os arquivos na pasta e subpastas
        for file in files:
            if is_image_file(file):  # Verifica se o arquivo é uma imagem com base na extensão
                file_path = os.path.join(root, file)  # Cria o caminho completo para o arquivo
                avg_rgb = calculate_average_rgb(file_path)  # Calcula a média RGB da imagem
                # Adiciona um dicionário com o caminho do arquivo e a média RGB à lista
                files_info.append({
                    'path': file_path,
                    'average_rgb': avg_rgb  # Armazena a média RGB calculada
                })
    return files_info  # Retorna a lista com as informações de todos os arquivos encontrados

def list_files():
    # Função principal que solicita ao usuário a pasta a ser analisada e lista os arquivos de imagem
    folder_path = select_folder()  # Permite que o usuário escolha uma pasta
    if folder_path and os.path.isdir(folder_path):  # Verifica se a pasta é válida
        # Lista os arquivos de imagem na pasta selecionada e subpastas
        files = list_files_recursively(folder_path)
        return files  # Retorna a lista de arquivos de imagem e suas médias RGB
    else:
        return []  # Retorna uma lista vazia se a pasta for inválida ou não selecionada

if __name__ == '__main__':
    # Se o script for executado diretamente, chama a função list_files para testar
    files = list_files()  # Chama a função para listar os arquivos
    print(json.dumps(files))  # Converte a lista de arquivos em JSON e imprime na saída padrão