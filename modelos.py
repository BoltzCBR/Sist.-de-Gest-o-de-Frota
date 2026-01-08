# Requisito 1: Classes e Herança
class Veiculo:
    def __init__(self, marca_escolhida, preco_inicial):
        self.marca = marca_escolhida 
        self.preco = float(preco_inicial)
        # Marcador para controlar se o desconto já foi usado
        self.ja_tem_desconto = False  

    def __str__(self):
        # Se tiver desconto, avisa na listagem
        etiqueta_promo = " [PROMOÇÃO]" if self.ja_tem_desconto else ""
        return f"{self.marca} | {self.preco:.2f}€{etiqueta_promo}"

class CarroEletrico(Veiculo):
    def __init__(self, marca, preco, capacidade_bateria):
        super().__init__(marca, preco)
        self.bateria = capacidade_bateria 

    def calcular_autonomia(self):
        # Cálculo simples: cada unidade de bateria dá 5.5km
        return self.bateria * 5.5