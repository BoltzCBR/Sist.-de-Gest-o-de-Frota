class Veiculo:
    def __init__(self, marca_escolhida, preco_inicial):
        self.marca = marca_escolhida 
        self.preco = float(preco_inicial)
        # Atributo de controlo para impedir múltiplos descontos no mesmo objeto
        self.ja_tem_desconto = False  

    def __str__(self):
        """
        O método __str__ define como o objeto aparece quando fazemos str(veiculo)
        ou quando o imprimimos na interface.
        """
        etiqueta_promo = " [PROMOÇÃO]" if self.ja_tem_desconto else ""
        # :.2f garante que o preço aparece sempre com 2 casas decimais
        return f"{self.marca} | {self.preco:.2f}€{etiqueta_promo}"

# Requisito: Herança
class CarroEletrico(Veiculo):
    def __init__(self, marca, preco, capacidade_bateria):
        # super() chama o construtor da classe pai (Veiculo)
        super().__init__(marca, preco)
        self.bateria = capacidade_bateria