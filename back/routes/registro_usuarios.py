from flask import Blueprint, jsonify, request
from db import get_db_connection

registro_usuarios_bp = Blueprint("registro_usuarios", __name__)

@registro_usuarios_bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT id_usuario, nombre, email, fecha_creacion
    FROM usuarios
    """

    cursor.execute(query)
    usuarios = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(usuarios), 200

@registro_usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT id_usuario, nombre, email, fecha_creacion
    FROM usuarios
    WHERE id_usuario = %s
    """

    cursor.execute(query, (id_usuario,))
    usuario = cursor.fetchone()

    cursor.close()
    connection.close()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario), 200

@registro_usuarios_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not nombre or not email or not password:
        return jsonify({"error": "No puede haber campos vacios"}), 400
    
    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"error": "Email invalido"}), 400
    
    if len(password) < 4:
        return jsonify({"error": "La contraseña debe contener al menos 4 caracteres"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try: 
        query = """
        INSERT INTO usuarios (nombre, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (nombre, email, password))
        connection.commit()

    except Exception:
        return jsonify({"error": "El email ya esta registrado"}), 400
    
    finally:
        cursor.close()
        connection.close()
    
    return jsonify({
        "mensaje": "Usuario creado correctamente"
    }), 201

@registro_usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):

    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')

    if not nombre or not email:
        return jsonify({"error": "Se debe completar el email y el nombre"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE usuarios
    SET nombre = %s, email = %s
    WHERE id_usuario = %s
    """

    cursor.execute(query, (nombre, email, id_usuario))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "mensaje": "Usuario actualizado"
    }), 200

@registro_usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "DELETE FROM usuarios WHERE id_usuario = %s"

    cursor.execute(query, (id_usuario,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "mensaje": "Usuario eliminado"
    }), 200

@registro_usuarios_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "El email y la contraseña son obligatorios"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT id_usuario, nombre, email
    FROM usuarios
    WHERE email = %s AND password = %s
    """

    cursor.execute(query, (email, password))
    usuario = cursor.fetchone()

    cursor.close()
    connection.close()

    if not usuario:
        return jsonify({
            "error": "Email o contraseña incorrectos"
        }), 401

    return jsonify({
        "mensaje": "Login exitoso",
        "usuario": usuario
    }), 200