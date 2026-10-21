from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select

from database import SessionLocal
from models import Livro, Usuario

app = Flask(__name__)


@app.route("/")
def index():
    session = SessionLocal()
    usuarios = session.scalars(select(Usuario)).all()
    livros = session.scalars(select(Livro)).all()
    return render_template("index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        if nome and email:
            session = SessionLocal()
            usuario = session.scalars(select(Usuario).where(User.email==email))

            else:
                return redirect(url_for('new_user'))

    return redirect(url_for('/'))
        

@app.route("/usuario/novo", methods=["POST","GET"])
def new_user():
    if request.method == "POST":
        nome = request.form.get("nome", None)
        email = request.form.get("email", None)

        if nome and email:
            session = SessionLocal()
            usuario = session.scalars(select(Usuario).where(Usuario.email==email))

            if not usuario:
                usuario_novo = Usuario(nome=nome, email=email)
                session.add(usuario_novo)
                session.commit()

            else:
                return redirect(url_for('login'))

@app.route("/livros/novo", methods=["POST","GET"])
def new_book():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        user_id = request.form.get("usuario_id")

        if titulo and user_id:
            session = SessionLocal()
            livro = session.scalars(select(Livro).where(Livro.titulo == titulo)).first()

            if not livro:
                livro_novo = Livro(titulo=titulo, user_id=int(usuario_id))
                session.add(livro_novo)
                session.commit()
                return redirect(url_for("listar_livro"))

    return render_template("cadastro_livro.html")

@app.route("/livros/listar")
def listar_livro():
    session = SessionLocal()
    livros = session.scalars(select(Livro).order_by(Livro.titulo)).all()
    return render_template("livros.html", livros=livros)


@app.route("/usuarios/listar")
def listar_usuarios():
    session = SessionLocal()
    usuarios = session.scalars(select(Usuario).order_by(Usuario.nome)).all()
    return render_template("index.html", usuarios=usuarios)

@app.route("/logout")
def logout():
    session.pop("usuario",None)
    return redirect(url_for('index'))

    


if __name__ == "main":
    app.run(debug=True)


