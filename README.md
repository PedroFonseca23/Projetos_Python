# 📊 Sistema de Orçamento Pessoal (Desktop App)

<img width="447" height="597" alt="image" src="https://github.com/user-attachments/assets/a1481174-f8ff-41b5-b9af-9aa27ec0bbfe" />


## 📖 Sobre o Projeto

Este é um projeto de um Sistema de Orçamento Pessoal de desktop, desenvolvido em Python. A aplicação permite ao usuário gerenciar suas finanças, registrando receitas e despesas, visualizando um histórico completo e analisando seus gastos através de um gráfico de pizza em tempo real.

O projeto foi construído com foco em criar uma interface gráfica (GUI) fluida e responsiva, utilizando PySimpleGUI, e em integrar visualização de dados com Matplotlib.

## ✨ Funcionalidades Principais
* **Gerenciamento (CRUD):**
    * **Adicionar:** Permite registrar novas transações (receitas ou despesas) com data, categoria e valor.
    * **Visualizar:** Exibe todas as transações em uma tabela detalhada no histórico.
    * **Deletar:** Permite deletar transações indesejadas com um clique (após seleção na tabela).
* **Persistência de Dados:** Todas as transações são salvas localmente em um arquivo `orcamento.json`, permitindo que os dados do usuário sejam mantidos entre as sessões.
* **Filtragem de Histórico:** O usuário pode filtrar o histórico de transações por um intervalo de datas específico ("De:" e "Até:").

## 🛠️ Tecnologias Utilizadas

* **Python 3.13**
* **PySimpleGUI (v5.x):** Para a criação de toda a interface gráfica de desktop.
* **Matplotlib:** Para a geração e exibição do gráfico de pizza.

---

## 🚀 Como Executar o Projeto

Para rodar este projeto em sua máquina local, siga os passos abaixo:


Criar e Ativar um Ambiente Virtual (Venv): (Isso é crucial para isolar as dependências)


# Criar o venv
python -m venv venv

# Ativar o venv (Windows)
.\venv\Scripts\Activate

 Instalar as Dependências: É altamente recomendado criar um arquivo requirements.txt.



# Dentro do venv ativado:
pip install matplotlib
pip install --upgrade --extra-index-url [https://PySimpleGUI.net/install](https://PySimpleGUI.net/install) PySimpleGUI

# (Opcional) Crie o arquivo requirements.txt para o futuro
pip freeze > requirements.txt
(Se o repositório já tiver o requirements.txt, basta rodar pip install -r requirements.txt)

 Executar a Aplicação:



# Certifique-se de que o venv está ativo!

python app_desktop.py

📦 Como Compilar para um .exe (Windows)

Uma das grandes vitórias deste projeto foi compilar um executável que pode ser distribuído para qualquer pessoa (mesmo sem Python instalado).

1. Instalar o PyInstaller (dentro do venv):


pip install pyinstaller

 Rodar o Comando de Compilação: (Use o comando que chama o pyinstaller.exe de dentro do venv para evitar conflitos de PATH)



.\venv\Scripts\pyinstaller.exe --windowed app_desktop.py

 Encontrar seu Aplicativo: Seu aplicativo estará pronto dentro da pasta dist/app_desktop. Você pode copiar esta pasta inteira para qualquer lugar, e o app_desktop.exe dentro dela irá funcionar.

📄 Licença
Este projeto está sob a licença MIT.

A parte do venv, e totalmente necessaria, pois necessita da pasta _internal que so vem apos a troca para .exe
