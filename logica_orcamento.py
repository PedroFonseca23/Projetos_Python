import json
from datetime import date

# Voltamos ao arquivo JSON simples
NOME_ARQUIVO = 'orcamento.json'

def carregar_dados():
    """Tenta carregar as transações do arquivo JSON."""
    try:
        with open(NOME_ARQUIVO, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Se o arquivo não existe, começa com uma lista vazia
        return []
    except json.JSONDecodeError:
        # Se o arquivo está corrompido ou vazio, começa do zero
        return []

def salvar_dados(transacoes):
    """Salva a lista de transações no arquivo JSON."""
    try:
        with open(NOME_ARQUIVO, 'w') as f:
            json.dump(transacoes, f, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return False

# --- Funções de Lógica ---

def adicionar_transacao_e_salvar(transacoes_lista, tipo, valor, categoria, data_str):
    """Adiciona uma transação a uma lista e salva no JSON."""
    try:
        valor_float = float(valor)
        if valor_float <= 0:
            return False, "O valor deve ser positivo."
        if not data_str:
            return False, "A data não pode estar vazia."

        transacao = {
            "tipo": tipo,
            "valor": valor_float,
            "categoria": categoria,
            "data": data_str
        }
        transacoes_lista.append(transacao)
        
        # Salva a lista principal atualizada
        salvar_dados(transacoes_lista) 
        
        return True, f"{tipo.capitalize()} de R$ {valor_float:.2f} adicionada."
    except ValueError:
        return False, "Valor inválido. Deve ser um número."

def deletar_transacao_e_salvar(transacoes_lista, indice_para_deletar):
    """Deleta uma transação de uma lista e salva no JSON."""
    try:
        transacoes_lista.pop(indice_para_deletar)
        
        # Salva a lista principal atualizada
        salvar_dados(transacoes_lista) 
        
        return True, "Transação deletada."
    except IndexError:
        return False, "Erro: Índice da transação não encontrado."

def get_resumo_from_list(lista_de_transacoes):
    """Calcula o resumo de uma lista de transações (filtrada ou não)."""
    total_receitas = 0
    total_despesas = 0
    gastos_por_categoria = {}

    for t in lista_de_transacoes:
        if t['tipo'] == 'receita':
            total_receitas += t['valor']
        elif t['tipo'] == 'despesa':
            total_despesas += t['valor']
            categoria = t['categoria'].upper() # Padroniza para maiúsculas
            gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0) + t['valor']

    saldo = total_receitas - total_despesas
    
    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo,
        "gastos_por_categoria": gastos_por_categoria
    }

def filtrar_transacoes(transacoes, data_inicio, data_fim):
    """Retorna uma nova lista de transações dentro do intervalo de datas."""
    if not data_inicio: data_inicio = "0000-01-01"
    if not data_fim: data_fim = "9999-12-31"
        
    transacoes_filtradas = []
    for t in transacoes:
        if data_inicio <= t['data'] <= data_fim:
            transacoes_filtradas.append(t)
            
    return transacoes_filtradas