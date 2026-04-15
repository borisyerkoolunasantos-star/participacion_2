from Flask import Flask, render_template, request, redirect
import sqlite3
#
app = Flask(__name__)

# Crear conexión
def get_db():
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    return conn

# Crear tabla automáticamente
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT,
            fecha_nac TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# LISTAR
@app.route('/')
def index():
    conn = get_db()
    personas = conn.execute("SELECT * FROM personas").fetchall()
    conn.close()
    return render_template("index.html", personas=personas)

# CREAR
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        fecha = request.form['fecha']

        conn = get_db()
        conn.execute("INSERT INTO personas (nombre, telefono, fecha_nac) VALUES (?, ?, ?)",
                     (nombre, telefono, fecha))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template("create.html")

# EDITAR
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()

    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        fecha = request.form['fecha']

        conn.execute("UPDATE personas SET nombre=?, telefono=?, fecha_nac=? WHERE id=?",
                     (nombre, telefono, fecha, id))
        conn.commit()
        conn.close()
        return redirect('/')

    persona = conn.execute("SELECT * FROM personas WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", persona=persona)

# ELIMINAR
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM personas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)