from flask import Flask, render_template, redirect, url_for, request, session
import requests
import os
from functools import wraps

API_BACKEND = os.environ.get("API_BACKEND", "http://127.0.0.1:5002")
app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    responce = requests.get(f'{API_BACKEND}/carta')
    platos = responce.json()
    response_populares = requests.get(f'{API_BACKEND}/menu/populares')
    platos_populares = response_populares.json()
    
    ids_platos_populares = [plato["id_plato"] for plato in platos_populares]
    return render_template("Menu.html", platos=platos, ids_platos_populares=ids_platos_populares)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        datos = {
                "nombre": request.form["nombre"],
                "email": request.form["email"],
                "password": request.form["password"]
            }
        respuesta = requests.post(f"{API_BACKEND}/usuarios",json=datos)
        
        if respuesta.status_code == 201:
                return redirect(url_for("login"))
        
        data = respuesta.json()

        return render_template(
            "registro.html",
            error = data.get("error"),
            nombre=datos["nombre"],
            email=datos["email"]
        )
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        datos = {
            "email": request.form["email"],
            "password": request.form["password"]
        }

        respuesta = requests.post(f"{API_BACKEND}/login", json=datos)

        if respuesta.status_code == 200:
            usuario = respuesta.json()["usuario"]

            session["usuario"] = usuario  

            return render_template("login_hecho.html", usuario=usuario)

        return render_template(
            "login.html",
            error="Email o contraseña incorrectos. Si no tienes cuenta, debes registrarte."
        )

    return render_template("login.html")

@app.route("/reservaciones", methods=["GET", "POST"])
def reservaciones():
    if request.method == "POST":

        if "usuario" not in session:
            return render_template(
                "reservas.html",
                reservas=[],
                error="Debes iniciar sesión para reservar"
            )


        fecha_reserva = request.form["fecha_reserva"]
        turno = request.form["turno"]
        cant_personas = int(request.form["cant_personas"])

        datos = {
            "id_usuario": session["usuario"]["id_usuario"],
            "fecha_reserva": fecha_reserva,
            "turno": turno,
            "cant_personas": cant_personas
        }

        respuesta = requests.post(f"{API_BACKEND}/reservas",json=datos)

        if respuesta.status_code == 201:
            id_usuario = session["usuario"]["id_usuario"]

            response = requests.get(f"{API_BACKEND}/reservas/usuario/{id_usuario}")
            reservas = response.json()
            return render_template(
                "reservas.html",
                reservas=reservas,
                exito="Reserva realizada con éxito"
        )
        
        data = respuesta.json()

        id_usuario = session["usuario"]["id_usuario"]

        response = requests.get(f"{API_BACKEND}/reservas/usuario/{id_usuario}")
        reservas = response.json()

        return render_template(
            "reservas.html",
            reservas=reservas,
            error=data.get("error"),
            fecha_reserva=fecha_reserva,
            turno=turno,
            cant_personas=cant_personas
        )

    if "usuario" in session:

        id_usuario = session["usuario"]["id_usuario"]

        response = requests.get(
            f"{API_BACKEND}/reservas/usuario/{id_usuario}"
        )

        reservas = response.json()

    else:
        reservas = []

    exito = request.args.get("exito")

    return render_template(
        "reservas.html",
        reservas=reservas,
        exito=exito
    )

@app.route("/cancelar_reserva/<int:id>")
def cancelar_reserva_front(id):

    requests.get(f"{API_BACKEND}/reservas/cancelar/{id}")

    return redirect(url_for("reservaciones", exito="Reserva cancelada"))

@app.route("/reseñas", methods=["GET", "POST"])
def reseñas():

    response = requests.get(f"{API_BACKEND}/resenias")
    reseñas = response.json()

    response_platos = requests.get(f"{API_BACKEND}/carta")
    platos = response_platos.json()

    reservas_usuario = []

    if "usuario" in session:
        id_usuario = session["usuario"]["id_usuario"]

        response_reservas = requests.get(
            f"{API_BACKEND}/reservas/usuario/{id_usuario}"
        )

        reservas_usuario = response_reservas.json()

    if request.method == "POST":

        if "usuario" not in session:
            return render_template(
                "reseñas.html",
                reseñas=reseñas,
                platos=platos,
                error="Debes iniciar sesión para dejar una reseña."
            )

        comentario = request.form["comentario"]
        puntaje_estrellas = request.form.get("puntaje_estrellas")
        id_plato = request.form.get("id_plato")
        id_reserva = request.form.get("id_reserva")

        if not puntaje_estrellas:
            return render_template(
                "reseñas.html",
                reseñas=reseñas,
                platos=platos,
                reservas_usuario=reservas_usuario,
                error="Debes seleccionar una cantidad de estrellas."
            )


        data = {
            "id_reserva": int(id_reserva),
            "id_plato": int(id_plato),
            "comentario": comentario,
            "puntaje_estrellas": int(puntaje_estrellas)
        }

        respuesta = requests.post(f"{API_BACKEND}/resenias", json=data)

        if respuesta.status_code != 201:
            return render_template(
                "reseñas.html",
                reseñas=reseñas,
                platos=platos,
                reservas_usuario=reservas_usuario,
                error="Debes reservar para poder dejar una reseña."
            )

        return redirect(url_for("reseñas"))

    return render_template("reseñas.html", reseñas=reseñas, platos=platos, reservas_usuario=reservas_usuario)


@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

@app.route("/logout")
def logout():
    session.clear() 
    return redirect(url_for("index"))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin")
@admin_required
def admin():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    return render_template("admin/dashboard.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        datos_admin = {
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
        respuesta = requests.post(f"{API_BACKEND}/login", json=datos_admin)        
        if respuesta.status_code == 200:
            session["admin"]=True
            return redirect(url_for("admin"))
        else:
            return "Login fallido", 401       
    return render_template('admin/login.html')

@app.route("/admin/registro", methods=["GET", "POST"])
def admin_registro():
    if request.method == "POST":
        datos_registro = {
            "nombre": request.form.get("nombre"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
        respuesta = requests.post(f"{API_BACKEND}/usuarios", json=datos_registro)
        if respuesta.status_code == 201:
            return redirect(url_for("admin_login"))
    return render_template("admin/registro.html")

@app.route("/admin/menu", methods=["GET", "POST"])
@admin_required
def admin_menu():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        datos_plato = {
            "nombre": request.form.get("nombre"),
            "precio": request.form.get("precio"),
            "categoria": request.form.get("categoria"),
            "descripcion": request.form.get("descripcion")
        }

        respuesta = requests.post(f"{API_BACKEND}/admin/menu", json=datos_plato)
        if respuesta.status_code == 201:
            return redirect(url_for("admin_menu"))
        return "Error al agregar plato al servidor", 500
    respuesta = requests.get(f"{API_BACKEND}/carta")
    lista_platos = respuesta.json()
    return render_template("admin/menu.html", platos=lista_platos)

@app.route("/admin/reservas")
@admin_required
def admin_reservas():
    respuesta = requests.get(f"{API_BACKEND}/reservas")
    lista_reservas = respuesta.json()
    return render_template("admin/reservas.html", reservas=lista_reservas)

@app.route("/admin/historial_reservas")
@admin_required
def admin_historial_reservas():
    respuesta = requests.get(f"{API_BACKEND}/reservas")
    historial_reservas = respuesta.json()
    return render_template("admin/historial_reservas.html", historial_reservas=historial_reservas)

@app.route("/admin/reseñas")
@admin_required
def admin_reseñas():
    respuesta = requests.get(f"{API_BACKEND}/resenias")

    lista_reseñas = respuesta.json()
    return render_template("admin/reseñas.html", reseñas=lista_reseñas)

@app.route("/admin/reseñas/eliminar/<int:id_resena>", methods=["POST"])
@admin_required
def admin_resena_eliminar(id_resena):
    requests.delete(f"{API_BACKEND}/admin/reseñas/{id_resena}")
    return redirect(url_for("admin_reseñas"))

@app.route("/admin/reseñas/editar/<int:id_resena>", methods=["GET", "POST"])
@admin_required
def admin_resena_editar(id_resena):
    if request.method == "POST":
        datos_reseña = {
            "comentario": request.form.get("comentario"),
            "puntaje_estrellas": int(request.form.get("puntaje_estrellas"))
        }

        requests.put(f"{API_BACKEND}/admin/reseñas/{id_resena}", json=datos_reseña)

        return redirect(url_for("admin_reseñas"))

    respuesta = requests.get(f"{API_BACKEND}/reseñas/{id_resena}")
    reseña = respuesta.json()
    return render_template("admin/editar_reseña.html", reseña=reseña)

@app.route("/admin/menu/borrar/<int:id_plato>", methods=["POST"])
@admin_required
def admin_menu_borrar(id_plato):
    requests.delete(f"{API_BACKEND}/admin/menu/{id_plato}")
    return redirect(url_for("admin_menu"))

@app.route("/admin/menu/editar/<int:id_plato>", methods=["GET", "POST"])
@admin_required
def admin_menu_editar(id_plato):
    if request.method == "POST":
        datos_plato = {
            "nombre": request.form.get("nombre"),
            "precio": request.form.get("precio"),
            "categoria": request.form.get("categoria"),
            "descripcion": request.form.get("descripcion")
        }
        requests.put(f"{API_BACKEND}/admin/menu/{id_plato}", json=datos_plato)
        
        return redirect(url_for("admin_menu"))
    respuesta = requests.get(f"{API_BACKEND}/carta/{id_plato}") 
    plato = respuesta.json()
    return render_template("admin/editar_plato.html", plato=plato)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)