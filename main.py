import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from modelos import Veiculo
from utilitarios import log_operacao

class Frota:
    def __init__(self):
        self.lista_veiculos = []

    @log_operacao 
    def adicionar_veiculo(self, veiculo_objeto):
        self.lista_veiculos.append(veiculo_objeto)

    def exportar_para_txt(self): 
        with open("frota_final.txt", "w", encoding="utf-8") as arquivo:
            for veiculo in self.lista_veiculos:
                arquivo.write(str(veiculo) + "\n")
        return "Inventário exportado com sucesso para 'frota_final.txt'!"

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.frota_dados = Frota()
        self.setWindowTitle("Gestor de Frota Pro")
        self.setFixedSize(400, 550)
        
        # Estilo para visibilidade (Letra preta no input, branca nos avisos)
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f7; }
            QMessageBox { background-color: #2b2b2b; }
            QMessageBox QLabel { color: #ffffff; font-size: 14px; }
            QMessageBox QPushButton { background-color: #0071e3; color: white; min-width: 70px; padding: 5px; }
            QLabel { font-weight: bold; color: #1d1d1f; font-size: 13px; margin-top: 5px; }
            QLineEdit { padding: 10px; border: 1px solid #d2d2d7; border-radius: 8px; background-color: white; color: #000000; font-size: 14px; }
            QPushButton { background-color: #0071e3; color: white; border-radius: 10px; padding: 12px; font-weight: bold; font-size: 13px; margin-top: 5px; }
            QPushButton:hover { background-color: #0077ed; }
            QPushButton#btn_ver { background-color: #86868b; }
            QPushButton#btn_save { background-color: #34c759; }
        """)

        container_principal = QWidget()
        self.setCentralWidget(container_principal)
        layout_vertical = QVBoxLayout(container_principal)

        titulo_app = QLabel("SISTEMA DE GESTÃO DE FROTA")
        titulo_app.setStyleSheet("font-size: 18px; color: #0071e3; margin-bottom: 10px;")
        titulo_app.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_vertical.addWidget(titulo_app)

        layout_vertical.addWidget(QLabel("Marca do Veículo:"))
        self.entrada_marca = QLineEdit()
        self.entrada_marca.setPlaceholderText("Ex: Ferrari, BMW, Toyota...")
        layout_vertical.addWidget(self.entrada_marca)

        layout_vertical.addWidget(QLabel("Preço (€):"))
        self.entrada_preco = QLineEdit()
        self.entrada_preco.setPlaceholderText("Ex: 50000")
        layout_vertical.addWidget(self.entrada_preco)

        layout_vertical.addSpacing(20)

        # Botões
        self.botao_add = QPushButton("REGISTAR VEÍCULO")
        self.botao_ver = QPushButton("VER FROTA COMPLETA")
        self.botao_ver.setObjectName("btn_ver") 
        self.botao_desc = QPushButton("APLICAR DESCONTO 10% (LAMBDA)")
        self.botao_find = QPushButton("FILTRAR TOYOTAS (COMPREENSÃO)")
        self.botao_save = QPushButton("EXPORTAR INVENTÁRIO (.TXT)")
        self.botao_save.setObjectName("btn_save") 

        for botao in [self.botao_add, self.botao_ver, self.botao_desc, self.botao_find, self.botao_save]:
            layout_vertical.addWidget(botao)

        # Conectar Eventos
        self.botao_add.clicked.connect(self.metodo_adicionar)
        self.botao_ver.clicked.connect(self.metodo_mostrar_tudo)
        self.botao_desc.clicked.connect(self.metodo_aplicar_lambda)
        self.botao_find.clicked.connect(self.metodo_filtrar_toyotas)
        self.botao_save.clicked.connect(self.metodo_exportar_ficheiro)

    def metodo_adicionar(self):
        marca_texto = self.entrada_marca.text()
        preco_texto = self.entrada_preco.text()
        
        if marca_texto and preco_texto:
            try:
                novo_veiculo = Veiculo(marca_texto, float(preco_texto))
                self.frota_dados.adicionar_veiculo(novo_veiculo)
                QMessageBox.information(self, "Sucesso", f"O veículo {marca_texto} foi guardado!")
                self.entrada_marca.clear()
                self.entrada_preco.clear()
            except ValueError:
                QMessageBox.critical(self, "Erro", "Introduza um valor numérico no preço!")
        else:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")

    def metodo_mostrar_tudo(self):
        if not self.frota_dados.lista_veiculos:
            QMessageBox.information(self, "Frota", "A lista está vazia de momento.")
            return
        # Transforma a lista de objetos numa string gigante para exibir
        texto_completo = "\n".join([str(item) for item in self.frota_dados.lista_veiculos])
        QMessageBox.information(self, "Frota Completa", texto_completo)

    def metodo_aplicar_lambda(self):
        # Requisito 4: Lambda
        funcao_desconto = lambda valor: valor * 0.90
        contagem_aplicados = 0
        
        for veiculo in self.frota_dados.lista_veiculos:
            if not veiculo.ja_tem_desconto:
                veiculo.preco = funcao_desconto(veiculo.preco)
                veiculo.ja_tem_desconto = True
                contagem_aplicados += 1
        
        if contagem_aplicados > 0:
            QMessageBox.information(self, "Lambda", f"Desconto aplicado a {contagem_aplicados} novos veículos!")
        else:
            QMessageBox.warning(self, "Aviso", "Todos os veículos na lista já têm o desconto aplicado.")

    def metodo_filtrar_toyotas(self):
        # Requisito 5: List Comprehension
        lista_filtrada = [v for v in self.frota_dados.lista_veiculos if "toyota" in v.marca.lower()]
        
        if not lista_filtrada:
            QMessageBox.information(self, "Pesquisa", "Não encontrámos nenhum Toyota.")
        else:
            resultado_texto = "\n".join([str(t) for t in lista_filtrada])
            QMessageBox.information(self, "Filtro Toyota", resultado_texto)

    def metodo_exportar_ficheiro(self):
        mensagem_resultado = self.frota_dados.exportar_para_txt()
        QMessageBox.information(self, "Exportação", mensagem_resultado)

if __name__ == "__main__":
    aplicacao = QApplication(sys.argv)
    janela_app = Interface()
    janela_app.show()
    sys.exit(aplicacao.exec())