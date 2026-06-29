from flask import Blueprint, jsonify
from db import get_db_connection


platos_populares_bp = Blueprint("platos_populares", __name__)

UMBRAL_PROMEDIO = 4.2


@platos_populares_bp.route("/menu/populares", methods=["GET"])
def platos_populares():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        carta.*,
        platos_populares.promedio_estrellas,
        platos_populares.cantidad_reseñas
    FROM platos_populares
    INNER JOIN carta
        ON platos_populares.id_plato = carta.id_plato
    WHERE platos_populares.es_popular = TRUE
    ORDER BY platos_populares.promedio_estrellas DESC
    LIMIT 10
    """

    cursor.execute(query)
    resultado = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(resultado)


@platos_populares_bp.route("/menu/populares/actualizar", methods=["POST"])
def actualizar_platos_populares():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM platos_populares")

        query = """
        INSERT INTO platos_populares (
            id_plato,
            promedio_estrellas,
            cantidad_reseñas,
            es_popular
        )
        SELECT
            id_plato,
            ROUND(SUM(puntaje_estrellas) / COUNT(*), 2),
            COUNT(*),
            CASE
                WHEN SUM(puntaje_estrellas) / COUNT(*) >= %s THEN TRUE
                ELSE FALSE
            END
        FROM reseñas
        GROUP BY id_plato
        """

        cursor.execute(query, (UMBRAL_PROMEDIO,))
        connection.commit()

    except Exception as error:
        connection.rollback()

        cursor.close()
        connection.close()

        return jsonify({
            "error": "No se pudieron actualizar los platos populares",
            "detalle": str(error)
        }), 500

    cursor.close()
    connection.close()

    return jsonify({
        "mensaje": "Platos populares actualizados correctamente"
    }), 200