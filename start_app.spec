# -*- mode: python ; coding: utf-8 -*-
# O cabeçalho define que o arquivo é um script Python e usa codificação UTF-8.

# O arquivo `start_app.spec` é utilizado pelo PyInstaller para criar o executável da aplicação.

# A primeira parte do arquivo configura a análise do script Python.
a = Analysis(
    ['start_app.py'],  # Define o script de entrada para o PyInstaller (neste caso, 'start_app.py')
    pathex=[],  # Diretórios adicionais para pesquisa de módulos. Aqui está vazio, então usa o diretório atual.
    binaries=[],  # Lista de arquivos binários que devem ser incluídos no executável. Está vazio, então não há binários adicionais.
    datas=[  # Lista de arquivos de dados que serão incluídos no executável.
        ('agent.py', '.'),  # Inclui o arquivo 'agent.py' no diretório raiz do executável.
        ('images/Onde-salvei-lemure-preto.ico', 'images')  # Inclui o ícone no diretório 'images' do executável.
    ],
    hiddenimports=[],  # Módulos adicionais que o PyInstaller não detecta automaticamente. Está vazio.
    hookspath=[],  # Caminhos para pastas de hooks personalizados. Aqui está vazio, então não há hooks personalizados.
    hooksconfig={},  # Configurações para hooks personalizados. Está vazio, então não há configurações extras.
    runtime_hooks=[],  # Hooks de tempo de execução. Está vazio, então não há hooks de tempo de execução.
    excludes=[],  # Módulos a serem excluídos do executável. Está vazio, então todos os módulos necessários serão incluídos.
    noarchive=False,  # Se verdadeiro, não cria um arquivo compactado (archive) no executável. Neste caso, é falso.
    optimize=0,  # Define o nível de otimização do código. 0 significa sem otimização.
)

# A segunda parte do arquivo cria o arquivo `.pyz` (um arquivo ZIP contendo os módulos Python compilados).
pyz = PYZ(a.pure)  # Cria o arquivo PYZ com os módulos puros (código Python) da análise.

# A terceira parte cria o executável final usando a análise e o arquivo PYZ gerado.
exe = EXE(
    pyz,  # O arquivo PYZ gerado na análise.
    a.scripts,  # Scripts Python a serem incluídos no executável (no caso, 'start_app.py').
    a.binaries,  # Arquivos binários a serem incluídos (nenhum neste caso).
    a.datas,  # Dados a serem incluídos (os arquivos 'agent.py' e o ícone).
    [],  # Argumentos adicionais (nenhum neste caso).
    name='Agente - Onde Salvei',  # Nome do executável gerado.
    debug=False,  # Se verdadeiro, ativa o modo de depuração.
    bootloader_ignore_signals=False,  # Se verdadeiro, ignora sinais do sistema operacional durante a inicialização.
    strip=False,  # Se verdadeiro, remove informações de depuração do executável.
    upx=True,  # Ativa a compressão do executável usando UPX (reduz o tamanho do arquivo).
    upx_exclude=[],  # Arquivos que não devem ser comprimidos com UPX. Está vazio, então não há exclusões.
    runtime_tmpdir=None,  # Diretório temporário para a execução. Está vazio, então o padrão será usado.
    console=False,  # Se verdadeiro, o executável será uma aplicação de console (não é o caso aqui, pois é uma aplicação com GUI).
    disable_windowed_traceback=False,  # Se verdadeiro, desabilita os rastros de erro para aplicativos sem console.
    argv_emulation=False,  # Se verdadeiro, emula argumentos de linha de comando para o aplicativo.
    target_arch=None,  # Arquitetura do alvo. Está vazio, então será determinado automaticamente.
    codesign_identity=None,  # Identidade de assinatura de código (usado em sistemas como o macOS).
    entitlements_file=None,  # Arquivo de permissões (usado em sistemas como o macOS).
    icon='images/Onde-salvei-lemure-preto.ico',  # Define o ícone do executável (usando o arquivo '.ico' fornecido).
)