from flask import Flask, request, render_template_string
import sqlite3
import hashlib

app = Flask(__name__)
DB_NAME = "usuarios.db"


HTML_FORM = """
<!DOCTYPE html>
<html>
<head><title>Login - DRY7122</title></head>
<body style="font-family: Arial; max-width: 400px; margin: 60px auto;">
    <h2>Login - Examen Transversal DRY7122</h2>
    <form method="POST">
        <label>Usuario:</label><br>
        <input type="text" name="usuario" required><br><br>
        <label>Contraseña:</label><br>
        <input type="password" name="password" required><br><br>
        <button type="submit">Ingresar</button>
    </form>
    {% if mensaje %}
        <p style="color: {{ 'green' if exito else 'red' }};"><b>{{ mensaje }}</b></p>
    {% endif %}
</body>
</html>
"""

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def validar_usuario(nombre, password):
    """Verifica si el hash de la contraseña ingresada coincide con el guardado en BD."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (nombre,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado is None:
        return False

    hash_guardado = resultado[0]
    hash_ingresado = hash_password(password)
    return hash_guardado == hash_ingresado


@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = None
    exito = False

    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        if validar_usuario(usuario, password):
            mensaje = f"Acceso concedido. Bienvenido, {usuario}."
            exito = True
        else:
            mensaje = "Usuario o contraseña incorrectos."
            exito = False

    return render_template_string(HTML_FORM, mensaje=mensaje, exito=exito)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800, debug=True)