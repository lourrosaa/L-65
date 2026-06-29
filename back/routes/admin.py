from flask import Blueprint, request, jsonify
from db import get_db_connection

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route("/admin/registro", methods=["POST"])
def api_admin_registrar():
    datos = request.json
    nombre = datos.get("nombre")
    email = datos.get("email")
    password = datos.get("password")

    if not nombre or not email or not password:
        return jsonify({"mensaje": "error de datos"}), 400
    
    return jsonify({"mensaje": "registro correcto"}), 201

@admin_bp.route("/admin/menu", methods=["POST"])
def admin_menu():
    datos = request.json
    nombre = datos.get("nombre")
    precio = datos.get("precio")
    categoria = datos.get("categoria")    
    descripcion = datos.get("descripcion")   
    if not nombre or not precio or not categoria or not descripcion:
        return jsonify({"mensaje": "faltan datos"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO carta (nombre_plato, precio, categoria, descripcion) VALUES (%s, %s, %s, %s)"

    cursor.execute(query, (nombre, precio, categoria, descripcion))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"mensaje": "plato agregado correctamente"}), 201

@admin_bp.route("/admin/menu/<int:id_plato>", methods=["DELETE"])
def api_admin_menu_borrar(id_plato):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM carta WHERE id_plato = %s", (id_plato,))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"mensaje": "Plato borrado exitosamente"}), 200

@admin_bp.route("/admin/menu/<int:id_plato>", methods=["PUT"])
def api_admin_menu_editar(id_plato):
    datos = request.json

    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE carta SET nombre_plato=%s, precio=%s, categoria=%s, descripcion=%s WHERE id_plato=%s"
    cursor.execute(query, (datos["nombre"], datos["precio"], datos["categoria"], datos["descripcion"], id_plato))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"mensaje": "Plato actualizado"}), 200

@admin_bp.route("/admin/reseñas/<int:id_resena>", methods=["DELETE"])
def api_admin_resena_borrar(id_resena):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM reseñas WHERE id_reseña = %s", (id_resena,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"mensaje": "Reseña borrada exitosamente"}), 200

@admin_bp.route("/admin/reseñas/<int:id_resena>", methods=["PUT"])
def api_admin_resena_editar(id_resena):
    datos = request.json

    connection = get_db_connection()
    cursor = connection.cursor()
    query = """ UPDATE reseñas SET comentario = %s, puntaje_estrellas = %s WHERE id_reseña = %s"""
    cursor.execute(query, (datos["comentario"], datos["puntaje_estrellas"], id_resena))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"mensaje": "Reseña actualizada"}), 200