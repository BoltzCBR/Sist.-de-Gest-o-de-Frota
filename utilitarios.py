from datetime import datetime

# Requisito: Decorador
def log_operacao(funcao_original):
    """
    Um decorador 'embrulha' uma função existente para adicionar lógica extra.
    Aqui, ele regista automaticamente quando qualquer método é chamado.
    """
    def embrulho_da_funcao(*args, **kwargs):
        # Captura a hora atual formatada
        agora = datetime.now().strftime("%H:%M:%S")
        
        # funcao_original.__name__ extrai o nome do método (ex: adicionar_veiculo)
        print(f" LOG [{agora}] -> A executar método: {funcao_original.__name__}")
        
        # Retorna a execução da função original com os seus argumentos
        return funcao_original(*args, **kwargs)
    
    return embrulho_da_funcao