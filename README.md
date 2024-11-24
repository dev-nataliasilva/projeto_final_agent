## Módulo de Agent Desktop - projeto _Onde Salvei_?
O Agent Desktop é uma aplicação desenvolvida para listar imagens em uma pasta selecionada pelo usuário, calcular a média das cores das imagens (em formato RGB) e exibir essas informações. A aplicação oferece uma interface gráfica para o usuário escolher a pasta e um ícone no sistema tray para interagir com o serviço.

### 📋 Estrutura do Projeto
- agent.py: Este script permite ao usuário selecionar uma pasta onde estão armazenadas imagens. Ele percorre a pasta e suas subpastas, calcula a média de cores (RGB) de cada imagem e retorna a lista de imagens e suas médias RGB.
- start_app.py: Este script cria um ícone no sistema tray e expõe um servidor Flask para iniciar o processo de busca de imagens via agent.py. Ele também permite que a aplicação seja adicionada à inicialização do Windows e oferece um menu simples com uma opção de "Sair".

### ⚙️ Funcionalidades
- Seleção de Pasta: O start_app.py permite ao usuário selecionar uma pasta onde as imagens estão localizadas. O agent.py percorre a pasta e suas subpastas, encontrando arquivos de imagem válidos.
- Cálculo da Média RGB: Para cada imagem, a média das cores RGB é calculada e retornada.
- Ícone no System Tray: O start_app.py cria um ícone no System Tray, permitindo ao usuário iniciar a busca de imagens com um clique. O script Flask é usado para controlar a execução.
- Adicionando à Inicialização do Windows: O start_app.py inclui uma funcionalidade que adiciona o aplicativo à inicialização do Windows, para que ele seja executado automaticamente toda vez que o computador for iniciado.

### 🚀 Como Executar
- Requisitos:
    - Python 3.8+
- Pacotes listados no arquivo requirements.txt. Para instalá-los, execute:
```python
pip install -r requirements.txt
```

#### Modo de Desenvolvimento
Para rodar o projeto em modo de desenvolvimento, execute o script start_app.py:
```bash
python start_app.py
```
Isso iniciará um servidor Flask e um ícone no System Tray. O servidor ficará aguardando requisições na rota /start_app, que ao ser acessada iniciará o processo de listagem de imagens.

#### Modo Standalone (Empacotado)
Para criar um executável independente (standalone), use o PyInstaller. Isso cria um arquivo executável que pode ser rodado diretamente sem a necessidade de instalar o Python ou as dependências. O executável será chamado _Agente - Onde Salvei_ e pode ser executado diretamente. Ele iniciará o processo de buscar imagens e gerar o ícone no System Tray. Crie o build com o seguinte comando:
```bash
pyinstaller start_app.spec
```
Isso gerará o executável na pasta dist/.

### 📝 Licença
Este projeto está sob a licença MIT. Sinta-se livre para utilizá-lo e modificá-lo conforme necessário.

### 🎓 Objetivo
Este código integra o ecossistema do produto _Onde Salvei?_, desenvolvido como parte do Projeto de Conclusão de Curso da graduação em Ciência da Computação.
