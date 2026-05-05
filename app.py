import sqlite3

app = Flask(__name__)
app.secret_key = 'Unaclavesecreta'

# Funcion para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect("bd_instituto.db")
    conn.row_factory = sqlite3.Row
    return conn
  
    
@app.route("/")
def index():
    return redirect(url_for('estudiantes'))

@app.route("/estudiantes")
def estudiantes():
    conn = get_db_connection()
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    conn.close()
    return render_template('estudiantes.html', estudiantes=estudiantes)

@app.route("/cursos")
def cursos():
    conn = get_db_connection()
    cursos = conn.execute('SELECT * FROM cursos').fetchall()
    conn.close()
    return render_template('cursos.html', cursos=cursos)
  
@app.route("/curso/nuevo", methods=['GET', 'POST'])
def nuevo_curso():
    if request.method == 'POST':
        # Leer contenido del formulario
        descripcion = request.form['descripcion']
        horas = request.form['horas']

        conn = get_db_connection()
        conn.execute("INSERT INTO cursos (descripcion, horas) VALUES (?,?)",(descripcion, horas))
        
        conn.commit()
        conn.close()
        flash('Curso agregado correctamente', 'success')
        return redirect(url_for('cursos'))
    return render_template('form_curso.html')
    
@app.route('/curso/editar/<int:id>', methods=['GET', 'POST'])
def editar_curso(id):
    conn = get_db_connection()
    curso = conn.execute("SELECT * FROM Curso WHERE id = ?", (id,)).fetchone()
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        horas = request.form['horas']
    
        conn.execute("UPDATE cursos SET descripcion = ?, horas = ? WHERE id = ?",(descripcion, horas, id))
        conn.commit()
        conn.close()
        flash('Curso actualizado', 'success')
        return redirect(url_for('cursos'))

    return render_template('form_curso.html', curso=curso)
    
@app.route('/curso/eliminar/<int:id>')
def eliminar_curso(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM cursos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Curso eliminado','success')
    return redirect(url_for('cursos'))
    
@app.route("/inscripciones")
def inscripciones():
    conn = get_db_connection()
    inscripciones = conn.execute(
      """
      SELECT i.id,
          i.fecha,
          e.nombre || ' ' || e.apellidos as estudiante,
          c.descripcion as curso
      FROM inscripciones i
      JOIN estudiantes e ON i.estudiante_id = e.id
      JOIN cursos c ON i.curso_id = c.id
      """
      ).fetchall()
    conn.close()
    return render_template('inscripciones.html', inscripciones=inscripciones)

@app.route("/inscripción/nuevo", methods=['GET', 'POST'])
def nueva_inscripción():
    conn = get_db_connection()
    # En caso de que sea POST, consolidar la inscripción
if request.method == 'POST':
    fecha = request.form['fecha']
    estudiante_id = request.form['estudiante_id']
    curso_id = request.form['curso_id']

    conn.execute(
        """
        INSERT INTO inscripciones
        (fecha, estudiante_id, curso_id)
        VALUES (?, ?, ?)
        """
    )
    conn.commit()
    conn.close()
    return redirect(url_for("inscripciones"))

    # En caso de GET Enviar datos para mostrar el formulario de inscripción
    estudiantes = conn.execute(
    """
    SELECT id, concat(nombre,'', apellidos) as nombre
    FROM estudiantes
    """
    ).fetchall()
cursos = conn.execute(
    """
    SELECT id, descripcion FROM cursos
    """
).foreach(c)
conn.close()
return render_template('form_inscripcion.html', estudiantes=estudiantes, cursos=cursos)
@app.route('/inscripcion/eliminar/<int:id>')

def eliminar_inscripcion(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM inscripciones WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('inscripciones'))

if __name__ == "__main__":
    app.run(debug=True)
