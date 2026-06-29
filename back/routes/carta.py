from flask import  Blueprint, jsonify, request
from db import get_db_connection

carta_bp = Blueprint("carta",__name__)

@carta_bp.route("/carta", methods=["GET"])
def mostrar_carta():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM carta"

    cursor.execute(query)
    carta = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(carta)

@carta_bp.route("/carta/<int:id>", methods=["GET"])
def mostrar_plato(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM carta WHERE id_plato = %s"
    cursor.execute(query, (id,))
    plato = cursor.fetchone()
    cursor.close()
    connection.close()

    if plato:
        return jsonify(plato),200
    return jsonify({
        "error": "Plato no encontrado"
    }), 404

@carta_bp.route("/carta/categoria/<categoria>", methods=["GET"])
def categoria_plato(categoria):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM carta WHERE categoria = %s"
    cursor.execute(query, (categoria,))
    resultado = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(resultado)