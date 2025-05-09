import sqlite3

class AppBd():
    def __init__(self):
        self.criar_tabela_alunos()
        self.criar_tabela_pagamentos()

    def abrir_conexao(self):
        try:
            self.connect = sqlite3.connect("database.db")
        except sqlite3.Error as erro:
            print(f"Ocorreu um erro ao abrir o banco de dodos {erro}")

    def fechar_conexao(self):
        try:
            self.connect.close()
            print("Banco foi fechado com sucesso")
        except sqlite3.Error as erro:
            print(f"falha ao fechar o banco {erro}")

    def criar_tabela_alunos(self):
        create_table_query = """ CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY, 
                                                                    nome TEXT NOT NULL, 
                                                                    endereco TEXT NOT NULL,
                                                                    cidade TEXT NOT NULL,
                                                                    estado TEXT NOT NULL CHECK (LENGTH(estado) = 2),
                                                                    telefone TEXT NOT NULL UNIQUE,
                                                                    status TEXT NOT NULL,
                                                                    data_matricula DATE,
                                                                    data_vencimento DATE,
                                                                    data_desligamento DATE);
                                                                    """
        self.abrir_conexao()

        try:
            cursor = self.connect.cursor()
            cursor.execute(create_table_query)
            self.connect.commit()
        except sqlite3.Error as erro:
            print(f"falha ao criar a tabela {erro}")
        finally:
            if self.connect:
                cursor.close()
                self.fechar_conexao()

    def inserir_aluno(self, nome, endereco, cidade, estado, telefone, status="cadastrado", data_matricula=None, data_vencimento=None, data_desligamento=None):
        insert_query = """INSERT INTO alunos (nome, endereco, cidade, estado, telefone, status, data_matricula, data_vencimento, data_desligamento)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        self.abrir_conexao()
        try:
            cursor = self.connect.cursor()
            cursor.execute(insert_query, (nome, endereco, cidade, estado, telefone, status, data_matricula, data_vencimento, data_desligamento))
            self.connect.commit()
            print("Aluno inserido com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao inserir aluno: {erro}")
        finally:
            cursor.close()
            self.fechar_conexao()

    def listar_alunos(self):
        self.abrir_conexao()
        select_query = """ SELECT * FROM alunos """
        alunos = []

        try:
            cursor = self.connect.cursor()
            cursor.execute(select_query)
            alunos = cursor.fetchall()
        except sqlite3.Error as erro:
             print(f"falha ao listar os dados{erro}")
        finally:
            if self.connect:
                cursor.close()
                self.fechar_conexao()
            return alunos
    
    def atualizar_dados_aluno(self, id_aluno, nome, endereco, cidade, estado, telefone):
        update_query = """UPDATE alunos SET nome=?, endereco=?, cidade=?, estado=?, telefone=?
                          WHERE id=?"""
        self.abrir_conexao()
        try:
            cursor = self.connect.cursor()
            cursor.execute(update_query, (nome, endereco, cidade, estado, telefone, id_aluno))
            self.connect.commit()
            print("Aluno atualizado com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao atualizar aluno: {erro}")
        finally:
            cursor.close()
            self.fechar_conexao()

    def atualizar_status_aluno(self, id_aluno, status, data_matricula, data_vencimento, data_desligamento):
        update_query = """UPDATE alunos SET status=?, data_matricula=?, data_vencimento=?, data_desligamento=? 
                          WHERE id=?"""
        self.abrir_conexao()
        try:
            cursor = self.connect.cursor()
            cursor.execute(update_query, (status, data_matricula, data_vencimento, data_desligamento, id_aluno))
            self.connect.commit()
            print("Aluno atualizado com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao atualizar aluno: {erro}")
        finally:
            cursor.close()
            self.fechar_conexao()

    def deletar_aluno(self,id_aluno):
        self.abrir_conexao()
        delete_query = """ DELETE FROM alunos WHERE id = ?"""
        try:
            cursor = self.connect.cursor()
            cursor.execute(delete_query, (id_aluno,))
            self.connect.commit()
            print("Aluno deletado com sucesso")
        except sqlite3.Error as erro:
            print(f"falha a deletar aluno {erro}")
        finally:
            if self.connect:
                cursor.close()
                self.fechar_conexao()

    def criar_tabela_pagamentos(self):
        create_table_query = """ CREATE TABLE IF NOT EXISTS pagamentos(id_pagamentos INTEGER PRIMARY KEY,
                                                                        data_pagamento DATE NOT NULL,
                                                                        id_aluno INTEGER NOT NULL,
                                                                        valor_pagamento REAL NOT NULL,
                                                                        tipo_pagamento TEXT NOT NULL,
                                                                        FOREIGN KEY (id_aluno) REFERENCES alunos(id))"""
        self.abrir_conexao()
        try:
            cursor = self.connect.cursor()
            cursor.execute(create_table_query)
            self.connect.commit()
        except sqlite3.Error as erro:
            print(f"Falha ao criar a tabela pagamentos: {erro}")
        finally:
            if self.connect:
                cursor.close()
                self.fechar_conexao()
    
    def inserir_pagamento(self, id_aluno, data, valor, tipo):
        self.abrir_conexao()
        insert_query = """ INSERT INTO pagamentos (id_aluno, data_pagamento, valor_pagamento, tipo_pagamento) VALUES (?, ?, ?, ?);"""

        try:
            cursor = self.connect.cursor()
            cursor.execute(insert_query, (id_aluno, data, valor, tipo))
            self.connect.commit()
            print("Pagamento inserido com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao inserir pagamento: {erro}")
        finally:
            cursor.close()
            self.fechar_conexao()
        
    def listar_pagamentos(self, id_aluno):
        self.abrir_conexao()
        select_query = """ SELECT * FROM pagamentos WHERE id_aluno = ?"""
        pagamentos = []
        
        try:
            cursor = self.connect.cursor()
            cursor.execute(select_query, (id_aluno,))
            pagamentos = cursor.fetchall()
        except sqlite3.Error as erro:
            print(f"Erro ao listar pagamentos: {erro}")
        finally:
            if self.connect:
                cursor.close()
                self.fechar_conexao()
            return pagamentos
        
    def atualizar_pagamento(self, id_pagamento, data, valor, tipo):
        self.abrir_conexao()
        update_query = """ UPDATE pagamentos SET data_pagamento = ?, valor_pagamento = ?, tipo_pagamento = ? WHERE id_pagamento = ? """
        
        try:
            cursor = self.connect.cursor()
            cursor.execute(update_query, (data, valor, tipo, id_pagamento))
            self.connect.commit()
            print("Pagamento atualizado com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao atualizar pagamento: {erro}")
        finally:
            cursor.close()
            self.fechar_conexao()
    
    def deletar_pagamento(self, id_aluno):
        delete_query = "DELETE FROM pagamentos WHERE id=?"
        self.abrir_conexao()
        try:
            cursor = self.connect.cursor()
            cursor.execute(delete_query, (id_aluno,))
            self.connect.commit()
            print("Pagamento deletado com sucesso!")
        except sqlite3.Error as erro:
            print(f"Erro ao deletar pagamento: {erro}")
        finally:
            cursor.close()
            self.fechar_conexao()



        