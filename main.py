import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from modelos import Veiculo
from utilitarios import log_operacao

class Frota:
    def __init__(self):
        # Base de dados em memória (lista de objetos da classe Veiculo)
        self.lista_veiculos = []

    @log_operacao # Aplicação do decorador para monitorizar registos
    def adicionar_veiculo(self, veiculo_objeto):
        self.lista_veiculos.append(veiculo_objeto)

    def exportar_para_txt(self): 
        # encoding="utf-8" é vital para suportar símbolos como o '€' no Windows
        with open("frota_final.txt", "w", encoding="utf-8") as arquivo:
            for veiculo in self.lista_veiculos:
                arquivo.write(str(veiculo) + "\n")
        return "Inventário exportado com sucesso!"

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.frota_dados = Frota()
        self.setWindowTitle("Gestor de Frota Pro")
        self.setFixedSize(400, 620)
        
        # QSS (Qt Style Sheets): Estilização da interface
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f7; }
            QLabel { font-weight: bold; color: #1d1d1f; font-size: 13px; margin-top: 5px; }
            QLineEdit { 
                padding: 10px; border: 1px solid #d2d2d7; border-radius: 8px; 
                background-color: #ffffff; color: #000000; font-size: 14px; 
            }
            QPushButton { 
                background-color: #0071e3; color: white; border-radius: 10px; 
                padding: 12px; font-weight: bold; border: none; 
            }
            QPushButton:hover { background-color: #0077ed; }
            QPushButton#btn_ver { background-color: #86868b; }
            QPushButton#btn_save { background-color: #34c759; }
            QPushButton#btn_filter { background-color: #f59e0b; }
            
            /* Garante que os pop-ups de aviso sejam legíveis (Fundo branco, letra preta) */
            QMessageBox { background-color: #ffffff; }
            QMessageBox QLabel { color: #000000; }
        """)

        # Configuração do Layout principal
        container_principal = QWidget()
        self.setCentralWidget(container_principal)
        layout_vertical = QVBoxLayout(container_principal)

        # Título
        titulo_app = QLabel("SISTEMA DE GESTÃO DE FROTA")
        titulo_app.setStyleSheet("font-size: 18px; color: #0071e3; margin-bottom: 10px;")
        titulo_app.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_vertical.addWidget(titulo_app)

        # Campos de entrada para registo
        layout_vertical.addWidget(QLabel("Marca do Veículo:"))
        self.entrada_marca = QLineEdit()
        layout_vertical.addWidget(self.entrada_marca)

        layout_vertical.addWidget(QLabel("Preço (€):"))
        self.entrada_preco = QLineEdit()
        layout_vertical.addWidget(self.entrada_preco)

        self.botao_add = QPushButton("REGISTAR VEÍCULO")
        layout_vertical.addWidget(self.botao_add)

        layout_vertical.addSpacing(20)
        
        # Campo de Pesquisa Dinâmica
        layout_vertical.addWidget(QLabel("Pesquisar Marca (Filtro):"))
        self.entrada_filtro = QLineEdit()
        self.entrada_filtro.setPlaceholderText("Ex: Escreva Toyota ou BMW...")
        layout_vertical.addWidget(self.entrada_filtro)

        self.botao_find = QPushButton("FILTRAR VEÍCULOS")
        self.botao_find.setObjectName("btn_filter")
        layout_vertical.addWidget(self.botao_find)

        layout_vertical.addSpacing(10)

        # Botões de visualização e sistema
        self.botao_ver = QPushButton("VER FROTA COMPLETA")
        self.botao_ver.setObjectName("btn_ver") 
        layout_vertical.addWidget(self.botao_ver)
        
        self.botao_desc = QPushButton("APLICAR DESCONTO 10% (LAMBDA)")
        layout_vertical.addWidget(self.botao_desc)
        
        self.botao_save = QPushButton("EXPORTAR INVENTÁRIO (.TXT)")
        self.botao_save.setObjectName("btn_save") 
        layout_vertical.addWidget(self.botao_save)

        # Conectar os cliques dos botões aos métodos (Funções)
        self.botao_add.clicked.connect(self.metodo_adicionar)
        self.botao_ver.clicked.connect(self.metodo_mostrar_tudo)
        self.botao_desc.clicked.connect(self.metodo_aplicar_lambda)
        self.botao_find.clicked.connect(self.metodo_filtrar_dinamico)
        self.botao_save.clicked.connect(self.metodo_exportar_ficheiro)

    def metodo_adicionar(self):
        marca = self.entrada_marca.text().strip()
        preco = self.entrada_preco.text().strip()
        
        if marca and preco:
            try:
                # Tentamos converter o preço para float. Se falhar, vai para o 'except'
                self.frota_dados.adicionar_veiculo(Veiculo(marca, float(preco)))
                QMessageBox.information(self, "Sucesso", f"O veículo {marca} foi guardado!")
                self.entrada_marca.clear()
                self.entrada_preco.clear()
            except ValueError:
                QMessageBox.critical(self, "Erro", "O preço tem de ser um número!")
        else:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")

    def metodo_mostrar_tudo(self):
        if not self.frota_dados.lista_veiculos:
            QMessageBox.information(self, "Frota", "A lista está vazia.")
            return
        # Transforma a lista de objetos numa única string para exibição
        res = "\n".join([str(v) for v in self.frota_dados.lista_veiculos])
        QMessageBox.information(self, "Frota Completa", res)

    def metodo_aplicar_lambda(self):
        """
        Requisito: Expressão Lambda
        Usa uma função anónima para calcular o desconto de 10%.
        """
        funcao_desconto = lambda valor: valor * 0.90
        count = 0
        for v in self.frota_dados.lista_veiculos:
            if not v.ja_tem_desconto:
                v.preco = funcao_desconto(v.preco)
                v.ja_tem_desconto = True
                count += 1
        QMessageBox.information(self, "Lambda", f"Desconto aplicado a {count} veículos novos.")

    def metodo_filtrar_dinamico(self):
        """
        Requisito: List Comprehension
        Cria uma sublista baseada no termo pesquisado.
        """
        termo = self.entrada_filtro.text().strip().lower()
        if not termo:
            QMessageBox.warning(self, "Aviso", "Escreva o nome de uma marca para filtrar!")
            return
        
        # Filtra a lista principal: mantém o veículo 'v' se o 'termo' estiver contido na 'marca'
        filtrados = [v for v in self.frota_dados.lista_veiculos if termo in v.marca.lower()]
        
        if filtrados:
            res = "\n".join([str(v) for v in filtrados])
            QMessageBox.information(self, f"Resultados para '{termo}'", res)
        else:
            QMessageBox.information(self, "Filtro", "Nenhum veículo corresponde à pesquisa.")

    def metodo_exportar_ficheiro(self):
        msg = self.frota_dados.exportar_para_txt()
        QMessageBox.information(self, "Exportar", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Interface()
    win.show()
    sys.exit(app.exec())