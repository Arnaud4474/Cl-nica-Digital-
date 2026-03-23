from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clinica_odonto_123"

def criar_banco():
    conn = sqlite3.connect("clinica.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            senha TEXT
        )
    """)
    conn.commit()
    conn.close()

criar_banco()

# Página inicial (painel)
@app.route("/")
def home():
    if "usuario" in session:
        return f"""
        <h1>🦷 Clínica Odontológica</h1>
        <h2>Bem-vindo, {session['usuario']}!</h2>
        <p>Sistema de pacientes ativo.</p>
        <a href='/logout'>Sair</a>
        """
    return redirect("/login")

# Cadastro de paciente
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pacientes (nome, senha) VALUES (?, ?)", (nome, senha))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("cadastro.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE nome=? AND senha=?", (nome, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["usuario"] = nome
            return redirect("/")
        else:
            return "Usuário ou senha inválidos ❌"

    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)