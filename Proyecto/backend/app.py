from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================
def get_db_connection():
    """Crea y retorna una conexión a la base de datos MySQL"""
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "root"),
        database=os.environ.get("DB_NAME", "robotica_db")
    )


# ============================================================
# RUTA DE PRUEBA - Health Check
# ============================================================
@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar que el servidor y la BD están funcionando"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return jsonify({
            "estado": "OK",
            "servidor": "Funcionando",
            "base_datos": "Conectada"
        }), 200
    except Exception as e:
        return jsonify({
            "estado": "ERROR",
            "servidor": "Funcionando",
            "base_datos": "Desconectada",
            "error": str(e)
        }), 500


# ============================================================
# 1. PROYECTO (CRUD)
# ============================================================

@app.route('/api/proyecto', methods=['GET'])
def obtener_proyectos():
    """Obtener todos los proyectos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM proyecto")
        proyectos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(proyectos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/proyecto/<int:id>', methods=['GET'])
def obtener_proyecto(id):
    """Obtener un proyecto por ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM proyecto WHERE id = %s", (id,))
        proyecto = cursor.fetchone()
        cursor.close()
        conn.close()

        if proyecto:
            return jsonify(proyecto), 200
        else:
            return jsonify({"error": "Proyecto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/proyecto', methods=['POST'])
def crear_proyecto():
    """Crear un nuevo proyecto"""
    try:
        data = request.get_json()

        campos_obligatorios = ['nombre', 'descripcion', 'objetivos', 'funcionamiento']
        for campo in campos_obligatorios:
            if campo not in data or not data[campo]:
                return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """INSERT INTO proyecto 
               (nombre, descripcion, objetivos, funcionamiento, aplicaciones, imagen_url) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                data['nombre'],
                data['descripcion'],
                data['objetivos'],
                data['funcionamiento'],
                data.get('aplicaciones', ''),
                data.get('imagen_url', '')
            )
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Proyecto creado exitosamente", "id": nuevo_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/proyecto/<int:id>', methods=['PUT'])
def actualizar_proyecto(id):
    """Actualizar un proyecto"""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM proyecto WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Proyecto no encontrado"}), 404

        cursor.execute(
            """UPDATE proyecto SET 
               nombre = %s, descripcion = %s, objetivos = %s, 
               funcionamiento = %s, aplicaciones = %s, imagen_url = %s
               WHERE id = %s""",
            (
                data.get('nombre', ''),
                data.get('descripcion', ''),
                data.get('objetivos', ''),
                data.get('funcionamiento', ''),
                data.get('aplicaciones', ''),
                data.get('imagen_url', ''),
                id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Proyecto actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/proyecto/<int:id>', methods=['DELETE'])
def eliminar_proyecto(id):
    """Eliminar un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM proyecto WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Proyecto no encontrado"}), 404

        cursor.execute("DELETE FROM proyecto WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Proyecto eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 2. COMPONENTES / MATERIALES (CRUD)
# ============================================================

@app.route('/api/componentes', methods=['GET'])
def obtener_componentes():
    """Obtener todos los componentes"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM componente")
        componentes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(componentes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/componentes/<int:id>', methods=['GET'])
def obtener_componente(id):
    """Obtener un componente por ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM componente WHERE id = %s", (id,))
        componente = cursor.fetchone()
        cursor.close()
        conn.close()

        if componente:
            return jsonify(componente), 200
        else:
            return jsonify({"error": "Componente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/componentes', methods=['POST'])
def crear_componente():
    """Crear un nuevo componente"""
    try:
        data = request.get_json()

        campos_obligatorios = ['nombre', 'tipo', 'descripcion']
        for campo in campos_obligatorios:
            if campo not in data or not data[campo]:
                return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """INSERT INTO componente 
               (nombre, tipo, descripcion, cantidad, imagen_url, proyecto_id) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                data['nombre'],
                data['tipo'],
                data['descripcion'],
                data.get('cantidad', 1),
                data.get('imagen_url', ''),
                data.get('proyecto_id', None)
            )
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Componente creado exitosamente", "id": nuevo_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/componentes/<int:id>', methods=['PUT'])
def actualizar_componente(id):
    """Actualizar un componente"""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM componente WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Componente no encontrado"}), 404

        cursor.execute(
            """UPDATE componente SET 
               nombre = %s, tipo = %s, descripcion = %s, 
               cantidad = %s, imagen_url = %s, proyecto_id = %s
               WHERE id = %s""",
            (
                data.get('nombre', ''),
                data.get('tipo', ''),
                data.get('descripcion', ''),
                data.get('cantidad', 1),
                data.get('imagen_url', ''),
                data.get('proyecto_id', None),
                id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Componente actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/componentes/<int:id>', methods=['DELETE'])
def eliminar_componente(id):
    """Eliminar un componente"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM componente WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Componente no encontrado"}), 404

        cursor.execute("DELETE FROM componente WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Componente eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 3. FOTOGRAFÍAS (CRUD)
# ============================================================

@app.route('/api/fotografias', methods=['GET'])
def obtener_fotografias():
    """Obtener todas las fotografías"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fotografia")
        fotos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(fotos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/fotografias', methods=['POST'])
def crear_fotografia():
    """Crear una nueva fotografía"""
    try:
        data = request.get_json()

        if 'url' not in data or not data['url']:
            return jsonify({"error": "El campo 'url' es obligatorio"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """INSERT INTO fotografia (titulo, url, descripcion, proyecto_id) 
               VALUES (%s, %s, %s, %s)""",
            (
                data.get('titulo', ''),
                data['url'],
                data.get('descripcion', ''),
                data.get('proyecto_id', None)
            )
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Fotografía creada exitosamente", "id": nuevo_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/fotografias/<int:id>', methods=['DELETE'])
def eliminar_fotografia(id):
    """Eliminar una fotografía"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM fotografia WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Fotografía eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 4. MANTENIMIENTO PREVENTIVO (CRUD)
# ============================================================

@app.route('/api/mantenimiento', methods=['GET'])
def obtener_mantenimiento():
    """Obtener todas las guías de mantenimiento"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mantenimiento")
        mantenimientos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(mantenimientos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/mantenimiento', methods=['POST'])
def crear_mantenimiento():
    """Crear una guía de mantenimiento"""
    try:
        data = request.get_json()

        campos_obligatorios = ['titulo', 'descripcion', 'tipo']
        for campo in campos_obligatorios:
            if campo not in data or not data[campo]:
                return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """INSERT INTO mantenimiento (titulo, descripcion, tipo, frecuencia, pasos) 
               VALUES (%s, %s, %s, %s, %s)""",
            (
                data['titulo'],
                data['descripcion'],
                data['tipo'],
                data.get('frecuencia', ''),
                data.get('pasos', '')
            )
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Guía de mantenimiento creada", "id": nuevo_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/mantenimiento/<int:id>', methods=['PUT'])
def actualizar_mantenimiento(id):
    """Actualizar una guía de mantenimiento"""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM mantenimiento WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Registro no encontrado"}), 404

        cursor.execute(
            """UPDATE mantenimiento SET 
               titulo = %s, descripcion = %s, tipo = %s, 
               frecuencia = %s, pasos = %s
               WHERE id = %s""",
            (
                data.get('titulo', ''),
                data.get('descripcion', ''),
                data.get('tipo', ''),
                data.get('frecuencia', ''),
                data.get('pasos', ''),
                id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Mantenimiento actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/mantenimiento/<int:id>', methods=['DELETE'])
def eliminar_mantenimiento(id):
    """Eliminar una guía de mantenimiento"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM mantenimiento WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Mantenimiento eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 5. NORMAS DE SEGURIDAD (CRUD)
# ============================================================

@app.route('/api/seguridad', methods=['GET'])
def obtener_normas_seguridad():
    """Obtener todas las normas de seguridad"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM norma_seguridad")
        normas = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(normas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/seguridad', methods=['POST'])
def crear_norma_seguridad():
    """Crear una norma de seguridad"""
    try:
        data = request.get_json()

        campos_obligatorios = ['titulo', 'descripcion', 'categoria']
        for campo in campos_obligatorios:
            if campo not in data or not data[campo]:
                return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """INSERT INTO norma_seguridad (titulo, descripcion, categoria, prioridad) 
               VALUES (%s, %s, %s, %s)""",
            (
                data['titulo'],
                data['descripcion'],
                data['categoria'],
                data.get('prioridad', 'media')
            )
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Norma de seguridad creada", "id": nuevo_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/seguridad/<int:id>', methods=['PUT'])
def actualizar_norma_seguridad(id):
    """Actualizar una norma de seguridad"""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM norma_seguridad WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Norma no encontrada"}), 404

        cursor.execute(
            """UPDATE norma_seguridad SET 
               titulo = %s, descripcion = %s, categoria = %s, prioridad = %s
               WHERE id = %s""",
            (
                data.get('titulo', ''),
                data.get('descripcion', ''),
                data.get('categoria', ''),
                data.get('prioridad', 'media'),
                id
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Norma de seguridad actualizada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/seguridad/<int:id>', methods=['DELETE'])
def eliminar_norma_seguridad(id):
    """Eliminar una norma de seguridad"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM norma_seguridad WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Norma de seguridad eliminada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)