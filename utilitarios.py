from datetime import datetime

# Requisito 2: Decorador para registo de operações
def log_operacao(funcao_original):
    """
    Este decorador regista a data, hora e o nome de qualquer 
    função que seja executada no programa.
    """
    def embrulho_da_funcao(*argumentos_posicionais, **argumentos_nomeados):
        # Obtém o momento exato da execução
        agora = datetime.now().strftime("%H:%M:%S")
        
        # Imprime no terminal o nome da função que foi disparada
        print(f" LOG [{agora}] -> A executar: {funcao_original.__name__}")
        
        # Executa a função propriamente dita com os seus dados
        return funcao_original(*argumentos_posicionais, **argumentos_nomeados)
    
    return embrulho_da_funcao