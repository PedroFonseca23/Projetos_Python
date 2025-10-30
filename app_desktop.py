# app_desktop.py
import PySimpleGUI as sg
import logica_orcamento
import datetime

# --- Importações para o Gráfico ---
import matplotlib
matplotlib.use('TkAgg') # Informa ao Matplotlib para usar o backend do Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Usando a versão 4.60.5 que é gratuita e estável
# pip install PySimpleGUI==4.60.5 matplotlib
sg.theme('DarkBlue3') # Mantém o tema bonito

# Formato de data que vamos usar
FORMATO_DATA = '%Y-%m-%d'

# --- Funções do Gráfico ---

def criar_grafico_pizza(gastos_por_categoria):
    """Cria uma figura do Matplotlib com o gráfico de pizza."""
    if not gastos_por_categoria:
        fig = plt.figure(figsize=(4, 3))
        plt.text(0.5, 0.5, 'Sem dados de despesa', horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.gca().axis('off')
        return fig

    labels = gastos_por_categoria.keys()
    sizes = gastos_por_categoria.values()
    
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(111)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=140)
    ax.axis('equal')
    fig.tight_layout()
    return fig

def desenhar_figura_no_canvas(canvas_element, figure):
    """Apaga o gráfico antigo e desenha o novo no Canvas do PySimpleGUI."""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas_element)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def apagar_grafico_antigo(figure_agg):
    """Remove o widget do gráfico antigo para evitar sobreposição."""
    if figure_agg:
        figure_agg.get_tk_widget().forget()
    plt.close('all')


# --- Funções de Ajuda da Interface ---

def atualizar_tabela(window, lista_para_exibir):
    """Atualiza o elemento da Tabela com dados de uma lista."""
    dados_tabela = []
    for t in reversed(lista_para_exibir):
        dados_tabela.append([
            t['data'],
            t['tipo'],
            t['categoria'],
            f"{t['valor']:.2f}"
        ])
    window['-TABELA-'].update(values=dados_tabela)

def atualizar_parte_visual(window, lista_para_exibir, figure_agg_antigo):
    """Função única para atualizar Resumo, Categoria e Gráfico."""
    
    resumo = logica_orcamento.get_resumo_from_list(lista_para_exibir)
    
    window['-RECEITAS-'].update(f"Total Receitas: R$ {resumo['total_receitas']:.2f}")
    window['-DESPESAS-'].update(f"Total Despesas: R$ {resumo['total_despesas']:.2f}")
    window['-SALDO-'].update(f"Saldo Atual: R$ {resumo['saldo']:.2f}")
    
    gastos_formatado = ""
    for categoria, valor in resumo['gastos_por_categoria'].items():
        gastos_formatado += f"- {categoria}: R$ {valor:.2f}\n"
    if not gastos_formatado: gastos_formatado = "Nenhuma despesa registrada."
    window['-CATEGORIAS-'].update(gastos_formatado)
    
    apagar_grafico_antigo(figure_agg_antigo)
    
    figura_nova = criar_grafico_pizza(resumo['gastos_por_categoria'])
    figure_agg_novo = desenhar_figura_no_canvas(window['-CANVAS-'].TKCanvas, figura_nova)
    
    return figure_agg_novo


# --- Layout da Janela Principal ---

def criar_janela_principal():
    """Cria o layout das abas e retorna a janela principal."""
    
    # Aba 1: Visão Geral (Resumo + Gráfico)
    layout_tab_visao_geral = [
        [sg.Text("RESUMO FINANCEIRO", font=("Helvetica", 14))],
        [sg.Text("", size=(30,1), key='-RECEITAS-')],
        [sg.Text("", size=(30,1), key='-DESPESAS-')],
        [sg.Text("", size=(30,1), key='-SALDO-', font=("Helvetica", 12, "bold"))],
        [sg.HorizontalSeparator()],
        [sg.Text("GRÁFICO DE DESPESAS", font=("Helvetica", 14))],
        [sg.Canvas(key='-CANVAS-', size=(400, 300))]
    ]

    # Aba 2: Histórico (Filtro + Tabela)
    tabela_titulos = ["Data", "Tipo", "Categoria", "Valor (R$)"]
    layout_tab_historico = [
        [sg.Frame("Filtrar por Data", layout=[
            [sg.Text('De:'), sg.Input(key='-DATA-INICIO-', size=12), sg.CalendarButton('Data', target='-DATA-INICIO-', format=FORMATO_DATA)],
            [sg.Text('Até:'), sg.Input(key='-DATA-FIM-', size=12), sg.CalendarButton('Data', target='-DATA-FIM-', format=FORMATO_DATA)],
            [sg.Button('Filtrar', key='-FILTRAR-'), sg.Button('Limpar Filtro', key='-LIMPAR-FILTRO-')]
        ])],
        [sg.Table(
            values=[], headings=tabela_titulos, key='-TABELA-',
            auto_size_columns=False, col_widths=[10, 8, 15, 10],
            justification='right', num_rows=15, enable_events=True
        )],
        [sg.Button("Deletar Transação Selecionada", button_color=('white', 'red'), key='-DELETAR-', disabled=True)]
    ]
    
    # Aba 3: Adicionar (Formulário + Lista de Categorias)
    layout_tab_adicionar = [
        [sg.Text("Adicionar Transação", font=("Helvetica", 14))],
        [sg.Text("Tipo:"), sg.Combo(['Receita', 'Despesa'], key='-TIPO-', default_value='Despesa')],
        [sg.Text("Categoria:"), sg.InputText(key='-CATEGORIA-')],
        [sg.Text("Valor (R$):"), sg.InputText(key='-VALOR-', size=(10,1))],
        [sg.Text("Data:"), sg.Input(key='-DATA-', size=12), sg.CalendarButton('Escolher', target='-DATA-', format=FORMATO_DATA)],
        [sg.Button("Adicionar")],
        [sg.HorizontalSeparator()],
        [sg.Text("Gastos por Categoria (Visão Atual):", font=("Helvetica", 12))],
        [sg.Multiline(size=(35, 10), key='-CATEGORIAS-', disabled=True, no_scrollbar=True)]
    ]

    # Layout principal com o grupo de abas
    layout = [
        [sg.Text("Sistema de Orçamento Pessoal v5", font=("Helvetica", 18))],
        [sg.TabGroup([
            [sg.Tab('Visão Geral', layout_tab_visao_geral)],
            [sg.Tab('Histórico', layout_tab_historico)],
            [sg.Tab('Adicionar', layout_tab_adicionar)]
        ], key='-TABGROUP-')],
        [sg.Button("Sair")]
    ]
    
    return sg.Window("Meu Orçamento v5", layout, finalize=True)

# --- Função Principal (Main) ---

def main():
    
    # --- 1. CARREGAR DADOS ---
    transacoes_principais = logica_orcamento.carregar_dados()

    # --- 2. INICIAR JANELA PRINCIPAL ---
    window = criar_janela_principal()
    
    data_hoje_str = datetime.date.today().strftime(FORMATO_DATA)
    window['-DATA-'].update(data_hoje_str)

    # --- 3. VARIÁVEIS DE ESTADO ---
    lista_exibida = transacoes_principais
    indice_original_selecionado = None
    figure_agg_atual = None

    # --- 4. CARREGAR DADOS INICIAIS ---
    figure_agg_atual = atualizar_parte_visual(window, lista_exibida, None)
    atualizar_tabela(window, lista_exibida)

    # --- 5. LOOP DE EVENTOS ---
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
            
        if event == 'Adicionar':
            tipo = 'receita' if values['-TIPO-'] == 'Receita' else 'despesa'
            categoria = values['-CATEGORIA-']
            valor = values['-VALOR-']
            data = values['-DATA-']
            
            # Chama a nova função que adiciona E salva
            sucesso, mensagem = logica_orcamento.adicionar_transacao_e_salvar(
                transacoes_principais, tipo, valor, categoria, data
            )
            
            if sucesso:
                # Limpa os campos
                window['-CATEGORIA-'].update('')
                window['-VALOR-'].update('')
                window['-DATA-'].update(data_hoje_str)
                
                # Reseta a visão (limpa filtros)
                lista_exibida = transacoes_principais
                window['-DATA-INICIO-'].update('')
                window['-DATA-FIM-'].update('')
                
                # Atualiza toda a interface
                figure_agg_atual = atualizar_parte_visual(window, lista_exibida, figure_agg_atual)
                atualizar_tabela(window, lista_exibida)
                sg.popup_auto_close("Adicionado!", auto_close_duration=1)
            else:
                sg.popup_error("Erro!", mensagem)

        elif event == '-TABELA-':
            try:
                indice_tabela_clicada = values['-TABELA-'][0]
                item_clicado = list(reversed(lista_exibida))[indice_tabela_clicada]
                indice_original_selecionado = transacoes_principais.index(item_clicado)
                window['-DELETAR-'].update(disabled=False)
            except (IndexError, ValueError):
                indice_original_selecionado = None
                window['-DELETAR-'].update(disabled=True)

        elif event == '-DELETAR-':
            if indice_original_selecionado is not None:
                if sg.popup_yes_no("Tem certeza que deseja deletar esta transação?") == 'Yes':
                    
                    # Chama a nova função que deleta E salva
                    sucesso, msg = logica_orcamento.deletar_transacao_e_salvar(transacoes_principais, indice_original_selecionado)
                    
                    if sucesso:
                        # Reseta tudo
                        lista_exibida = transacoes_principais
                        indice_original_selecionado = None
                        window['-DELETAR-'].update(disabled=True)
                        window['-DATA-INICIO-'].update('')
                        window['-DATA-FIM-'].update('')
                        
                        figure_agg_atual = atualizar_parte_visual(window, lista_exibida, figure_agg_atual)
                        atualizar_tabela(window, lista_exibida)
                    else:
                        sg.popup_error("Erro!", msg)
            else:
                sg.popup_error("Erro!", "Nenhuma transação selecionada.")

        elif event == '-FILTRAR-':
            data_inicio = values['-DATA-INICIO-']
            data_fim = values['-DATA-FIM-']
            
            lista_exibida = logica_orcamento.filtrar_transacoes(transacoes_principais, data_inicio, data_fim)
            
            figure_agg_atual = atualizar_parte_visual(window, lista_exibida, figure_agg_atual)
            atualizar_tabela(window, lista_exibida)
            
            indice_original_selecionado = None
            window['-DELETAR-'].update(disabled=True)

        elif event == '-LIMPAR-FILTRO-':
            lista_exibida = transacoes_principais
            window['-DATA-INICIO-'].update('')
            window['-DATA-FIM-'].update('')
            
            figure_agg_atual = atualizar_parte_visual(window, lista_exibida, figure_agg_atual)
            atualizar_tabela(window, lista_exibida)
            
            indice_original_selecionado = None
            window['-DELETAR-'].update(disabled=True)

    window.close()


if __name__ == "__main__":
    main()