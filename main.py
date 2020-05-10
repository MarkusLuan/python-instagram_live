import instagram
import time
import flask
from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

stream = None
logado = False

@app.route("/login", methods=["GET"])
def login():
    if logado:
        return redirect("/")

    status = request.args.get("status")
    if status is None:
        status = ""

    return render_template("login.html", status=status)

@app.route("/login", methods=["POST"])
def fazerLogin():
    global logado

    if logado:
        return redirect("/")
    
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    try:
        instagram.fazerLogin(usuario, senha)
        logado = usuario

        return redirect("/")
    except:
        return redirect("/login?status=Login invalido!")

@app.route("/stream/criar")
def criarStream():
    global stream

    if not logado:
        print("Erro: Faça o login antes de tentar criar uma stream")
        return redirect("/login")

    stream = instagram.getStream()

    return redirect("/")

@app.route("/stream/iniciar")
def iniciarStream():
    if not logado:
        print("Erro: Faça o login antes de tentar iniciar uma stream")
        return redirect("/login")

    if stream is None:
        print("Erro: Você deve criar o stream antes de iniciar")
        return redirect("/?erro&mensagem=Você deve criar o stream antes de iniciar")
    
    stream.iniciar()
    return redirect("/")

@app.route("/stream/encerrar")
def encerrarStream():
    global stream
    
    if not logado:
        print("Erro: Faça o login antes de tentar encerrar uma stream")
        return redirect("/login")

    if stream is None:
        print("Erro: Não existe streams para encerrar")
        return redirect("/?erro&mensagem=Não existe streams para encerrar")

    stream.encerrar()
    stream = None
    return redirect ("/?mensagem=Stream encerrado!")

@app.route("/comentarios")
def getComentarios():
    lastComent = request.args.get("lastComent")

    comentarios = instagram.getComentarios(stream, lastComent)
    if (len(comentarios) > 0):
        print("Novos comentários")

    return json.dumps(comentarios)

@app.route("/")
def index():
    if not logado:
        return redirect("/login")

    erro = request.args.get("erro")
    mensagem = request.args.get("mensagem")

    return render_template("index.html", login=logado, stream=stream, erro=erro, mensagem=mensagem)

if __name__ == '__main__':
    app.run(port=80, debug=True)