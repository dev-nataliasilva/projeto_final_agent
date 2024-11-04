import os
from tkinter import Tk, filedialog

def select_folder():
    # Inicia a interface gráfica para seleção de pastas
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    folder_path = filedialog.askdirectory()  # Abre o diálogo para escolher uma pasta
    return folder_path

def list_files():
    folder_path = select_folder()  # Permite que o usuário escolha uma pasta
    if folder_path and os.path.isdir(folder_path):  # Se uma pasta foi selecionada e é válida
        # Listar arquivos na pasta selecionada e criar uma lista com o caminho completo
        files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
        return files  # Retorna a lista de arquivos
    else:
        return None  # Retorna None se a pasta for inválida

if __name__ == '__main__':
    files = list_files()  # Para testes locais, você pode chamar diretamente
    print(files)  # Para visualizar os arquivos encontrados
