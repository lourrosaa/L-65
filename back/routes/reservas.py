from flask import Blueprint, jsonify, request
from db import get_db_connection
import qrcode

import os
from dotenv import load_dotenv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

load_dotenv()

def enviar_email(destinatario, datos_qr, path_qr, link_cancelacion):
    remitente = os.getenv("EMAIL_RESERVAS")
    password = os.getenv("EMAIL_RESERVAS_CONTRASENIA")

    mensaje = MIMEMultipart("related")  #indica que manda un mail con varias partes relacionadas
    #headers del mail
    mensaje["Subject"] = "Reserva confirmada"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    html = f"""
    <h2>Reserva confirmada</h2>

    <p>{datos_qr}</p>

    <p>Mostrá este QR:</p>
    <img src="cid:qr">  

    <br><br>

    <a href="{link_cancelacion}">
        Cancelar reserva
    </a>
    """

    mensaje.attach(MIMEText(html, "html"))

    with open(path_qr, "rb") as f:
        img = MIMEImage(f.read()) 
        img.add_header("Content-ID", "<qr>") 
        mensaje.attach(img)  

    with smtplib.SMTP("smtp.gmail.com", 587) as server: 
        server.starttls()  
        server.login(remitente, password)
        server.send_message(mensaje)

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def mostrar_reservas():

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT reservas.*,usuarios.nombre FROM reservas 
    JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario
    WHERE reservas.estado = 'activa'
    ORDER BY reservas.fecha_reserva, reservas.turno
    """

    cursor.execute(query)

    reservas = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(reservas), 200


@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def mostrar_reserva_id(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT reservas.*,usuarios.nombre FROM reservas 
    JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario 
    WHERE reservas.id_reserva = %s
    AND reservas.estado = 'activa'
    """

    cursor.execute(query, (id,))

    reserva = cursor.fetchone()

    cursor.close()
    conn.close()

    if reserva:
        return jsonify(reserva), 200

    return jsonify({
        "error": "Reserva no encontrada"
    }), 404

@reservas_bp.route('/reservas/disponibilidad', methods=['GET'])
def ver_disponibilidad():

    fecha = request.args.get("fecha")

    if not fecha:
        return jsonify({"error": "Se necesita la fecha"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        #Consulto la capacidad en cada turno
        consulta = """
        SELECT turno, SUM(cant_personas) AS total
        FROM reservas
        WHERE fecha_reserva = %s
        AND estado = 'activa'
        GROUP BY turno
        """

        cursor.execute(consulta, (fecha,))
        resultados = cursor.fetchall()
    
        capacidad_max = 60
        respuesta = []

        for turno in ["20-22", "22-00"]:
            ocupado = 0

            for resultado in resultados:
                if resultado["turno"] == turno:
                    ocupado = resultado["total"] or 0

            respuesta.append({
                "turno": turno,
                "disponible": capacidad_max - ocupado
            })

        return jsonify(respuesta), 200

    except Exception as e:
        return jsonify({
            "error": "Error al buscar la disponibilidad",
            "detalle": str(e)
        }), 500
    
    finally:
        cursor.close()
        conn.close()

   
@reservas_bp.route('/reservas', methods=['POST'])
def crear_reserva():

    data = request.get_json()

    id_usuario = data.get('id_usuario')
    fecha_reserva = data.get('fecha_reserva')
    cant_personas = data.get('cant_personas')
    turno = data.get('turno')

    if not id_usuario or not fecha_reserva or not cant_personas or not turno:
        return jsonify({
            "error": "Faltan datos para crear la reserva"
        }), 400
    
    if turno not in ["20-22", "22-00"]:
        return jsonify ({"error": "Turno invalido"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        #Valido la disponibilidad
        check = """
        SELECT SUM(cant_personas) AS total
        FROM reservas
        WHERE fecha_reserva = %s
        AND turno = %s
        AND estado = 'activa'
        
        """

        cursor.execute(check, (fecha_reserva, turno))
        resultado = cursor.fetchone()
        ocupado = resultado["total"] or 0
        capacidad_max = 60

        if ocupado + cant_personas > capacidad_max:
            return jsonify({
                "error": "No hay disponibilidad para esta fecha"
            }), 400

        query = """
        INSERT INTO reservas (id_usuario, fecha_reserva, cant_personas, turno)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (id_usuario, fecha_reserva, cant_personas, turno))

        conn.commit()

        id_reserva = cursor.lastrowid  #Obtengo el id de la reserva
        
        datos_qr = f"""
            Reserva: {id_reserva}
            Usuario: {id_usuario}
            Fecha: {fecha_reserva}
            Turno: {turno}
            Personas: {cant_personas}
        """

        img_qr = qrcode.make(datos_qr)  #Agarra el texto y lo convierte en un codigo qr(imagen)

        path_qr = f"qr_reserva_{id_reserva}.png"  
        img_qr.save(path_qr) #Lo guarda como archivo imagen

        query_email = """
        SELECT email FROM usuarios WHERE id_usuario = %s
        """

        cursor.execute(query_email, (id_usuario,))
        usuario = cursor.fetchone()

        if not usuario: 
            return jsonify({"error": "Usuario no encontrado"}), 404

        usuario_email = usuario["email"]
        link_cancelacion = f"http://localhost:5000/reservas/cancelar/{id_reserva}"
        
        try: 
            enviar_email(usuario_email, datos_qr, path_qr, link_cancelacion) 
            print("MAIL ENVIADO") 
        except Exception as e: 
            print("ERROR MAIL:", e)

        return jsonify({
            "mensaje": "Reserva creada exitosamente",
            "id_reserva": id_reserva
        }), 201
    
    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": "Error con la reserva",
            "detalle": str(e)
        }), 500
    
    finally:
        cursor.close()
        conn.close()


@reservas_bp.route('/reservas/<int:id>', methods=['PUT'])
def actualizar_reserva(id):

    data = request.get_json()

    id_usuario = data.get('id_usuario')
    fecha_reserva = data.get('fecha_reserva')
    cant_personas = data.get('cant_personas')
    turno = data.get ('turno')

    if not id_usuario or not fecha_reserva or not cant_personas or not turno:
        return jsonify({
            "error": "Faltan datos para actualizar la reserva"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        #Valido la capacidad sin incluir la reserva actual
        check = """
        SELECT SUM(cant_personas) AS total
        FROM reservas
        WHERE fecha_reserva = %s
        AND id_reserva != %s
        AND turno = %s
        AND estado = 'activa'
        """

        cursor.execute(check, (fecha_reserva, id, turno))
        resultado = cursor.fetchone()
        ocupado = resultado["total"] or 0

        capacidad_max = 60

        if ocupado + cant_personas > capacidad_max:
            return jsonify ({
                "error": "No hay disponibilidad para esta fecha"
            }), 400

        query = """
        UPDATE reservas
        SET id_usuario = %s, fecha_reserva = %s, cant_personas = %s, turno = %s
        WHERE id_reserva = %s
        """

        cursor.execute(query, (id_usuario, fecha_reserva, cant_personas, turno, id))

        conn.commit()

        return jsonify({
            "mensaje": "Reserva actualizada exitosamente"
        }), 200
    
    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": "Error con la reserva",
            "detalle": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

@reservas_bp.route('/reservas/cancelar/<int:id>', methods=['GET'])
def cancelar_reserva(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    try: 
        check = """
        SELECT estado FROM reservas
        WHERE id_reserva = %s
        """

        cursor.execute(check, (id,))
        reserva = cursor.fetchone()

        if not reserva:
            return jsonify({"error": "Reserva no encontrada"}), 404
        
        if reserva["estado"] == "cancelada":
            return jsonify({"mensaje": "La reserva ya está cancelada"}), 400
        
        query = """
        UPDATE reservas SET estado = 'cancelada'
        WHERE id_reserva = %s
        """

        cursor.execute(query, (id,))
        conn.commit()

        return jsonify({
            "mensaje": "Reserva cancelada exitosamente"
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": "Error al cancelar la reserva",
            "detalle": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

        
@reservas_bp.route('/reservas/usuario/<int:id_usuario>', methods=['GET'])
def reservas_usuario(id_usuario):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM reservas
    WHERE id_usuario = %s
    AND estado = 'activa'
    """

    cursor.execute(query, (id_usuario,))
    reservas = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(reservas), 200