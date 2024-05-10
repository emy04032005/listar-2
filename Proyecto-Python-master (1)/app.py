from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__, template_folder='template')

# Función para conectar a la base de datos SQLite y crear las tablas si no existen
def create_tables():
    conn = sqlite3.connect('database/login.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    correo TEXT NOT NULL,
                    password TEXT NOT NULL,
                    id_rol INTEGER NOT NULL DEFAULT 2
                )''')
    conn.commit()
    conn.close()

# Función para obtener la conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('database/login.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta principal
  

# Ruta de administrador
@app.route('/admin')
def admin():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    conn.close()
    return render_template('admin.html', usuarios=usuarios)

# ACCESO - LOGIN
@app.route('/acceso-login', methods=["POST"])
def login():
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios WHERE correo = ? AND password = ?', (correo, password,))
    account = cur.fetchone()
  
    if account:
        session['logueado'] = True
        session['id'] = account['id']
        session['id_rol'] = account['id_rol']
        
        if session['id_rol'] == 1:
            return render_template("admin.html")
        elif session['id_rol'] == 2:
            return render_template("usuario.html")
    else:
        return render_template('index.html', mensaje="Usuario o Contraseña Incorrectas")

# Registro
@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/crear-registro', methods=["POST"])
def crear_registro(): 
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (correo, password) VALUES (?, ?)", (correo, password))
    conn.commit()
    conn.close()
    
    return render_template("index.html", mensaje2="Usuario Registrado Exitosamente")

@app.route('/veruser')
def veruser():
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT  id,correo  FROM usuarios")
    user = cur.fetchall()
    conn.close()
    
    return render_template('listar_usuarios.html',user=user)

if __name__ == '__main__':
    app.secret_key = "ok"
    create_tables()  # Llama a la función para crear las tablas al iniciar la aplicación
    