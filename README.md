#Projetos Python

📊 Sistema de Orçamento Pessoal (Desktop App)
(Importante: Tire um screenshot do seu aplicativo (como você me mandou) e faça o upload em algum lugar, como o Imgur, ou adicione-o à pasta do seu repositório. Em seguida, substitua o link acima.)

📖 Sobre o Projeto
Este é um projeto de um Sistema de Orçamento Pessoal de desktop, desenvolvido em Python. A aplicação permite ao usuário gerenciar suas finanças, registrando receitas e despesas, visualizando um histórico completo e analisando seus gastos através de um gráfico de pizza em tempo real.

O projeto foi construído com foco em criar uma interface gráfica (GUI) fluida e responsiva, utilizando PySimpleGUI, e em integrar visualização de dados com Matplotlib.

✨ Funcionalidades Principais
Interface Gráfica Moderna: Organizada em três abas (Visão Geral, Histórico, Adicionar) para uma navegação limpa e intuitiva.

Visualização de Dados: Gráfico de pizza em tempo real na aba "Visão Geral" que mostra a distribuição percentual de despesas por categoria.

Gerenciamento (CRUD):

Adicionar: Permite registrar novas transações (receitas ou despesas) com data, categoria e valor.

Visualizar: Exibe todas as transações em uma tabela detalhada no histórico.

Deletar: Permite deletar transações indesejadas com um clique (após seleção na tabela).

Persistência de Dados: Todas as transações são salvas localmente em um arquivo orcamento.json, permitindo que os dados do usuário sejam mantidos entre as sessões.

Filtragem de Histórico: O usuário pode filtrar o histórico de transações por um intervalo de datas específico ("De:" e "Até:").

🛠️ Tecnologias Utilizadas
Python 3.13

PySimpleGUI (v5.x): Para a criação de toda a interface gráfica de desktop.

Matplotlib: Para a geração e exibição do gráfico de pizza.

🚀 Como Executar o Projeto
Para rodar este projeto em sua máquina local, siga os passos abaixo:

1. Clonar o Repositório:

Bash

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
2. Criar e Ativar um Ambiente Virtual (Venv): (Isso é crucial para isolar as dependências)

Bash

# Criar o venv
python -m venv venv

# Ativar o venv (Windows)
.\venv\Scripts\Activate
3. Instalar as Dependências: Recomendamos criar um arquivo requirements.txt. Para fazer isso, rode:

Bash

# Dentro do venv ativado:
pip install matplotlib
pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI

# (Opcional) Crie o arquivo requirements.txt para o futuro
pip freeze > requirements.txt
(Se você já tiver o requirements.txt, basta rodar pip install -r requirements.txt)

4. Executar a Aplicação:

Bash

# Certifique-se de que o venv está ativo!
python app_desktop.py
📦 Como Compilar para um .exe (Windows)
Uma das grandes vitórias deste projeto foi compilar um executável que pode ser distribuído para qualquer pessoa (mesmo sem Python instalado).

1. Instalar o PyInstaller (dentro do venv):

Bash

pip install pyinstaller
2. Rodar o Comando de Compilação: (Use o comando que chama o pyinstaller.exe de dentro do venv para evitar conflitos de PATH)

Bash

.\venv\Scripts\pyinstaller.exe --windowed app_desktop.py
3. Encontrar seu Aplicativo: Seu aplicativo estará pronto dentro da pasta dist/app_desktop. Você pode copiar esta pasta inteira para qualquer lugar, e o app_desktop.exe dentro dela irá funcionar.
