import json
from datetime import date 


NOME_ARQUIVO = 'orcamento.json'

def carregar_dados():
    """Tenta carregar as transações do arquivo JSON."""
    try:
        with open(NOME_ARQUIVO, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
       
        return []
    except json.JSONDecodeError:
       
        return []

def salvar_dados(transacoes):
    """Salva a lista de transações no arquivo JSON."""
    with open(NOME_ARQUIVO, 'w') as f:
        
        json.dump(transacoes, f, indent=4)

def adicionar_transacao(transacoes, tipo):
    """Função genérica para adicionar receita ou despesa."""
    try:
        valor = float(input(f"Digite o valor da {tipo}: R$ "))
        categoria = input(f"Digite a categoria da {tipo} (ex: Salário, Comida, Transporte): ")
        
        if valor <= 0:
            print("O valor deve ser positivo.")
            return

       
        data_hoje = date.today().isoformat() 

        
        transacao = {
            "tipo": tipo,
            "valor": valor,
            "categoria": categoria,
            "data": data_hoje
        }
        
        
        transacoes.append(transacao)
        salvar_dados(transacoes) 
        print(f"{tipo.capitalize()} de R$ {valor:.2f} (Categoria: {categoria}) adicionada.")

    except ValueError:
        print("Valor inválido. Por favor, digite um número.")

def ver_resumo(transacoes):
    """Calcula e exibe o resumo financeiro."""
    
    total_receitas = 0
    total_despesas = 0
    
    
    gastos_por_categoria = {}

    for t in transacoes:
        if t['tipo'] == 'receita':
            total_receitas += t['valor']
        elif t['tipo'] == 'despesa':
            total_despesas += t['valor']
            
           
            categoria = t['categoria']
            if categoria in gastos_por_categoria:
                gastos_por_categoria[categoria] += t['valor']
            else:
                gastos_por_categoria[categoria] = t['valor']

    saldo = total_receitas - total_despesas
    
    print("\n--- Resumo do Orçamento ---")
    print(f"Total de Receitas: R$ {total_receitas:.2f}")
    print(f"Total de Despesas: R$ {total_despesas:.2f}")
    print("----------------------------")
    print(f"Saldo Atual: R$ {saldo:.2f}")
    
    
    if gastos_por_categoria:
        print("\n--- Gastos por Categoria ---")
        for categoria, valor in gastos_por_categoria.items():
            print(f"- {categoria}: R$ {valor:.2f}")

def main():
    """Função principal que executa o programa."""
    
    
    transacoes = carregar_dados()
    
    print("--- Calculadora de Orçamento Pessoal (v2) ---")
    print(f"Dados carregados de '{NOME_ARQUIVO}'")

    while True:
        print("\nO que você deseja fazer?")
        print("1 - Adicionar Receita")
        print("2 - Adicionar Despesa")
        print("3 - Ver Resumo")
        print("4 - Sair")
        
        escolha = input("Digite sua escolha (1/2/3/4): ")

        if escolha == '1':
            adicionar_transacao(transacoes, 'receita')

        elif escolha == '2':
            adicionar_transacao(transacoes, 'despesa')

        elif escolha == '3':
            ver_resumo(transacoes)
            
        elif escolha == '4':
           
            salvar_dados(transacoes)
            print("Encerrando o programa. Dados salvos. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, escolha 1, 2, 3 ou 4.")


if __name__ == "__main__":
    main()