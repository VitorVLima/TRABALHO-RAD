from app import app
from app.modelo import AppBd
from flask import render_template, url_for, request, redirect,flash
from datetime import datetime, timedelta

db = AppBd()

def atualizar_status_alunos():
    alunos = db.listar_alunos()
    hoje = datetime.today().date()

    for aluno in alunos:
        id_aluno = aluno[0]
        status = aluno[6]
        data_matricula = aluno[7]
        data_vencimento = aluno[8]
        data_desligamento = aluno[9]

        pagamentos = db.listar_pagamentos(id_aluno)

        if pagamentos == None:
            db.atualizar_status_aluno(
                id_aluno=id,
                status="cadastrado",
                data_matricula=None,
                data_vencimento=None,
                data_desligamento=None)
        
        else:

            if data_vencimento:
                vencimento = datetime.strptime(data_vencimento, "%Y-%m-%d").date()
                nova_data_desligamento = vencimento + timedelta(days=1)

                if hoje > vencimento and status != "pagamento atrasado":
                    db.atualizar_status_aluno(
                        id_aluno=id_aluno,
                        novo_status="pagamento atrasado",
                        data_matricula = None,
                        data_vencimento = None,
                        data_desligamento= nova_data_desligamento.strftime("%Y-%m-%d")
                    )



@app.route("/")
def homepage():
    atualizar_status_alunos()
    alunos = db.listar_alunos()
    return render_template("index.html", alunos = alunos, title = "Pagina Inicial")


@app.route("/cadastrar_aluno", methods=["GET", "POST"])
def cadastrar_aluno():
    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        telefone = request.form.get("telefone")

    
        if not (nome and endereco and cidade and estado and telefone):
            print("Preencha todos os campos")
            return redirect(url_for("cadastrar_aluno"))
    

        db.inserir_aluno(
            nome=nome,
            endereco=endereco,
            cidade=cidade,
            estado=estado,
            telefone=telefone
        )

        return redirect(url_for('homepage'))

    return render_template("cadastroaluno.html", title = "Cadastrar Aluno")

@app.route("/aluno/<int:id>", methods=["GET"])
def dados_aluno(id):
    
    alunos = db.listar_alunos()

    for a in alunos:
        if a[0] == id:
            aluno = a

    pagamentos = db.listar_pagamentos(id)

    if pagamentos == None:
        db.atualizar_status_aluno(
            id_aluno=id,
            status="cadastrado",
            data_matricula=None,
            data_vencimento=None,
            data_desligamento=None)
    

    return render_template('aluno.html', title = "Dados do Aluno", aluno = aluno, pagamentos = pagamentos)

@app.route("/atualizar/<int:id>", methods=["POST", "GET"])
def atualizar_dados_aluno(id):
    alunos = db.listar_alunos()

    for a in alunos:
        if a[0] == id:
            aluno = a

    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        telefone = request.form.get("telefone")

    
        if not (nome and endereco and cidade and estado and telefone):
            print("Preencha todos os campos")
            return redirect(url_for("atualizar_dados_aluno", id=id))
        
        db.atualizar_dados_aluno(
            id_aluno = id,
            nome=nome,
            endereco=endereco,
            cidade=cidade,
            estado=estado,
            telefone=telefone)
        
        return redirect(url_for("dados_aluno", id=id))

    
    return render_template('atualizaraluno.html', aluno = aluno)



@app.route("/pagamento/<int:id>", methods=["POST"])
def novo_pagamento(id):
    valor = float(request.form.get("valor", 100.00))
    tipo = request.form.get("tipo")

    if not valor or not tipo:
        print("Preencha todos os campos do pagamento!")
        return redirect(url_for("dados_aluno", id=id))
    
    if tipo != "Dinheiro" and  tipo != "Cartão":
        print("Tipo de pagamento não reconhecido. Selecione Cartão ou Dinheiro!")
        return redirect(url_for("dados_aluno", id=id))

    data_pagamento = datetime.today().strftime("%Y-%m-%d")
    db.inserir_pagamento(id_aluno=id, data=data_pagamento, valor=valor, tipo=tipo)

    alunos = db.listar_alunos()

    for a in alunos:
        if a[0] == id:
            aluno = a

    if aluno:
        data_matricula = aluno[7]
        data_vencimento_atual = aluno[8]

    if not data_matricula:
        data_matricula = data_pagamento

    if not data_vencimento_atual:
        data_vencimento_novo = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        vencimento = datetime.strptime(data_vencimento_atual, "%Y-%m-%d")
        data_vencimento_novo = (vencimento + timedelta(days=1)).strftime("%Y-%m-%d")

    db.atualizar_status_aluno(
            id_aluno=id,
            status="matriculado",
            data_matricula=data_matricula,
            data_vencimento=data_vencimento_novo,
            data_desligamento=None)
    return redirect(url_for('dados_aluno', id=id))


    
