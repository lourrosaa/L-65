from flask import Blueprint, jsonify, request
from db import get_db_connection

reseñas_bp = Blueprint("reseñas", __name__)

@reseñas_bp.route("/resenias", methods=["GET"])
def mostrar_reseñas():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT
        reseñas.*,
        carta.nombre_plato
    FROM reseñas
    JOIN carta
        ON reseñas.id_plato = carta.id_plato
    ORDER BY fecha DESC
    """

    cursor.execute(query)
    reseñas = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(reseñas)

@reseñas_bp.route("/resenias", methods=["POST"])
def crear_reseña():
    data = request.json

    id_reserva = data.get("id_reserva")
    comentario = data.get("comentario")
    puntaje = int(data.get("puntaje_estrellas"))
    id_plato = data.get("id_plato")

    obligatorio = ["id_reserva", "comentario", "puntaje_estrellas", "id_plato"]

    for campo in obligatorio:
        if campo not in data:
            return jsonify({"Error": f"Falta {campo}"}), 400

    if puntaje < 1 or puntaje > 5:
        return {"Error": "Puntaje invàlido"}, 400
    
    id_reserva = data.get("id_reserva")
    comentario = data.get("comentario")
    puntaje = int(data.get("puntaje_estrellas"))
    id_plato = data.get("id_plato")

    if puntaje < 1 or puntaje > 5:
        return jsonify({
            "Error": "Puntaje inválido"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM reservas WHERE id_reserva = %s"
        cursor.execute(query, (id_reserva,))
        reserva = cursor.fetchone()

        if not reserva:
            cursor.close()
            connection.close()
            return {"Error": "La reserva no existe"}, 404

        sql = "INSERT INTO reseñas (id_reserva, comentario, puntaje_estrellas, id_plato) VALUES (%s, %s, %s, %s)"

        cursor.execute(sql, (id_reserva, comentario, puntaje, id_plato))

        connection.commit()
        cursor.execute("DELETE FROM platos_populares")

        cursor.execute("""
            INSERT INTO platos_populares (
                id_plato,
                promedio_estrellas,
                cantidad_reseñas,
                es_popular
            )
            SELECT
                id_plato,
                ROUND(AVG(puntaje_estrellas), 2),
                COUNT(*),
                CASE
                    WHEN AVG(puntaje_estrellas) >= 4.2
                    THEN TRUE
                    ELSE FALSE
                END
            FROM reseñas
            GROUP BY id_plato
            """)

        connection.commit()
        
        return jsonify({"Mensaje": "Reseña creada con exito"}), 201
    except Exception as e:

        connection.rollback()

        return jsonify({
            "Error": "No se pudo crear la reseña",
            "detalle": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()

@reseñas_bp.route("/resenias/<int:id>", methods=["DELETE"])
def eliminar_reseña_id(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM reseñas WHERE id_reseña = %s"
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"Mensaje": "Reseña eliminada con exito"}, 200

@reseñas_bp.route("/reseñas/<int:id_resena>", methods=["GET"])
def obtener_reseña(id_resena):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reseñas WHERE id_reseña = %s", (id_resena,))
    reseña = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify(reseña)
