from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.core.text import LabelBase
from urllib.parse import quote
from datetime import datetime
import json
import os

def obtener_url_backend():
    ruta_config = 'config.json'
    if not os.path.exists(ruta_config):
        return 'http://127.0.0.1:5000'
        
    with open(ruta_config, 'r') as archivo:
        datos = json.load(archivo)
        return datos.get('BASE_URL', 'http://127.0.0.1:5000')

BASE_URL = obtener_url_backend()


LabelBase.register(
    name="MedievalSharp-Book",
    fn_regular='assets/fonts/MedievalSharp-Book.ttf'
)

class InicioScreen(Screen):
    def ir_a_carta_publica(self):
        self.manager.current = 'carta'
        self.manager.get_screen('carta').cargar_platos()


class CartaScreen(Screen):
    def seleccionar_categoria(self, boton):
        if 'lista_platos' in self.ids:
            self.ids.lista_platos.clear_widgets()

        categoria = boton.text

        categoria_filtrada = quote(categoria)
        
        if categoria != "Platos Populares":
            UrlRequest(
                f"{BASE_URL}/carta/categoria/{categoria_filtrada}",
                on_success=self.platos_cargados_ok,
                on_failure=lambda req, res: print("FAIL:", res),
                on_error=lambda req, err: print("ERROR:", err)
            )
        else:
            UrlRequest(
                f"{BASE_URL}/menu/populares",
                on_success=self.platos_cargados_ok,
                on_failure=lambda req, res: print("FAIL:", res),
                on_error=lambda req, err: print("ERROR:", err)
            )

    def cargar_platos(self):
        if 'lista_platos' in self.ids:
            self.ids.lista_platos.clear_widgets()
        
        UrlRequest(
            f"{BASE_URL}/carta",
            on_success=self.platos_cargados_ok,
            on_failure=self.error_carga,
            on_error=self.error_carga
        )

    def platos_cargados_ok(self, req, result):
        if 'lista_platos' not in self.ids:
            return
            
        platos = result
        if not platos:
            self.ids.lista_platos.add_widget(Label(text="No hay platos disponibles hoy.", size_hint_y=None, height=40))
            return

        for plato in platos:
            if isinstance(plato, dict):
                nombre = plato.get('nombre_plato', 'Plato sin nombre')
                precio = plato.get('precio', '')
            else:
                nombre = plato[1]
                precio = plato[3] if len(plato) > 3 else ""

            imagen_url = f"assets/images/{nombre}.jpg"

            texto_plato = f"{nombre} - ${precio}" if precio else f"{nombre}"

            item = Factory.CartaItem()
            item.texto = texto_plato
            item.imagen = imagen_url

            self.ids.lista_platos.add_widget(item)

    def error_carga(self, req, error):
        if 'lista_platos' in self.ids:
            self.ids.lista_platos.add_widget(Label(text="Error al conectar con el backend.", color=[1,0,0,1], size_hint_y=None, height=40))


class LoginScreen(Screen):
    def procesar_login(self, email, password):
        if not email or not password:
            self.ids.mensaje_estado.text = "Completa todos los campos."
            return

        paquete = {'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}
        
        UrlRequest(
            f"{BASE_URL}/login",
            req_body=json.dumps(paquete),
            req_headers=headers,
            on_success=self.login_exitoso,
            on_failure=self.login_fallido,
            on_error=self.conexion_error
        )

    def login_exitoso(self, req, result):
        user_data = result.get('usuario')
        user_id = user_data['id_usuario'] if isinstance(user_data, dict) else user_data[1]
        App.get_running_app().user_id = user_id
        nombre_usuario = user_data['nombre'] if isinstance(user_data, dict) else user_data[2]
        
        pantalla_principal = self.manager.get_screen('principal')
        pantalla_principal.ids.bienvenido_label.text = f"¡Hola, {nombre_usuario}!"
        
        self.manager.current = 'principal'
        self.ids.mensaje_estado.text = "" 

    def login_fallido(self, req, result):
        mensaje = result.get('mensaje', 'Credenciales incorrectas') if isinstance(result, dict) else "Error"
        self.ids.mensaje_estado.color = [1, 0, 0, 1]
        self.ids.mensaje_estado.text = mensaje

    def conexion_error(self, req, error):
        self.ids.mensaje_estado.color = [1, 0, 0, 1]
        self.ids.mensaje_estado.text = "No se pudo conectar con el servidor."


class RegistroScreen(Screen):
    def procesar_registro(self, nombre, email, password):
        if not nombre or not email or not password:
            self.ids.mensaje_registro.text = "Completa todos los campos."
            return

        paquete = {'nombre': nombre, 'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}

        UrlRequest(
            f"{BASE_URL}/usuarios",
            req_body=json.dumps(paquete),
            req_headers=headers,
            on_success=self.registro_exitoso,
            on_failure=self.registro_fallido,
            on_error=self.conexion_error
        )

    def registro_exitoso(self, req, result):
        self.manager.current = 'login'
        self.manager.get_screen('login').ids.mensaje_estado.color = [0, 1, 0, 1]
        self.manager.get_screen('login').ids.mensaje_estado.text = "¡Cuenta creada! Ya puedes ingresar."
        
        self.ids.nombre_input.text = ""
        self.ids.email_registro.text = ""
        self.ids.password_registro.text = ""

    def registro_fallido(self, req, result):
        self.ids.mensaje_registro.color = [1, 0, 0, 1]
        self.ids.mensaje_registro.text = "Error al registrar el usuario."

    def conexion_error(self, req, error):
        self.ids.mensaje_registro.color = [1, 0, 0, 1]
        self.ids.mensaje_registro.text = "Error de conexión."

class ReservasScreen(Screen):
    def obtener_fecha(self):
        fecha_str = self.ids.fecha_reserva_input.text

        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"Error: {e}")

    def crear_reserva(self, cant_personas):
        turno = self.ids.turno_input.text

        user_id = App.get_running_app().user_id

        fecha_reserva=self.obtener_fecha()

        cant_personas = int(cant_personas)

        if not cant_personas or not fecha_reserva or not turno or not user_id:
            self.ids.mensaje_reserva.text = "Completa todos los campos."
            print(cant_personas, fecha_reserva, turno, user_id)
            return
        
        print(cant_personas, fecha_reserva, turno, user_id)

        paquete = {"id_usuario": user_id, "cant_personas": cant_personas, "fecha_reserva": fecha_reserva, "turno": turno}
        headers = {'Content-Type': 'application/json'}

        UrlRequest(
            f"{BASE_URL}/reservas",
            req_body=json.dumps(paquete),
            req_headers=headers,
            on_success=self.reservas_cargadas_ok,
            on_failure=lambda req, res: print("FAIL:", res),
            on_error=lambda req, err: print("ERROR", err)
        )

    def cargar_reservas(self):
        if 'lista_reservas' in self.ids:
            self.ids.lista_reservas.clear_widgets()
        
        UrlRequest(
            f"{BASE_URL}/reservas",
            on_success=self.reservas_cargadas_ok,
            on_failure=self.error_carga,
            on_error=self.error_carga
        )
    def reservas_cargadas_ok(self, req, result):
        if 'lista_reservas' not in self.ids:
            return
        
        if not result:
            self.ids.lista_reservas.add_widget(Label(text="No tienes reservas activas.", size_hint_y=None, height=40))
            return
        
        reservas = result

        for reserva in reservas:
            fecha = reserva.get('fecha_reserva') if isinstance(reserva, dict) else reserva[2]
            hora = reserva.get('turno') if isinstance(reserva, dict) else reserva[3]
            cantidad = reserva.get('cant_personas') if isinstance(reserva, dict) else reserva[4]
            estado = reserva.get('estado') if isinstance(reserva, dict) else reserva[5]
            texto_reserva = f"{fecha} a las {hora} - {cantidad} personas - {estado}"
            
            item = Factory.ReseniaItem()
            item.texto = texto_reserva

            self.ids.lista_reservas.add_widget(item)

    def error_carga(self, req, error):
        if 'lista_reservas' in self.ids:
            self.ids.lista_reservas.add_widget(Label(text="Error al cargar tus reservas. (ERROR BACKEND)", color=[1,0,0,1], size_hint_y=None, height=40))


class ReseniaScreen(Screen):
    def crear_resenia(self, comentario):
        reserva = self.ids.drop_reservas.text

        puntuacion = self.ids.puntuacion.text

        plato = self.ids.drop_platos.text

        reserva = reserva.split("-")

        puntuacion = int(puntuacion)

        plato = plato.split("-")

        if not reserva or not plato or not comentario or not puntuacion:
            self.ids.mensaje_resenia.text = "Faltan datos para hacer la reseña"
            print(reserva, puntuacion, plato, comentario)
            return
        
        print(reserva, puntuacion, plato, comentario)

        paquete = {"id_reserva": reserva[0], "id_plato": plato[0], "comentario": comentario, "puntaje_estrellas": puntuacion}
        headers = {'Content-Type': 'application/json'}

        UrlRequest(
            f"{BASE_URL}/resenias",
            req_body=json.dumps(paquete),
            req_headers=headers,
            on_success=self.resenias_cargadas_ok,
            on_failure=lambda req, res: print("FAIL:", res),
            on_error=lambda req, err: print("ERROR", err)
        )
    
    def cargar_reservas(self):
        UrlRequest(f"{BASE_URL}/reservas", on_success=self.on_reservas)

    def on_reservas(self, req, result):
        self.reservas_map = {}

        lista = []
        for r in result:
            texto = f"{r['id_reserva']} - {r['fecha_reserva']}"
            lista.append(texto)
            self.reservas_map[texto] = r

        self.ids.drop_reservas.values = lista

    def cargar_platos(self):
        UrlRequest(f"{BASE_URL}/carta", on_success=self.on_platos)

    def on_platos(self, req, result):
        self.platos_map = {}

        lista = []
        for r in result:
            texto = f"{r['id_plato']}-{r['nombre_plato']}"
            lista.append(texto)
            self.platos_map[texto] = r

        self.ids.drop_platos.values = lista

    def cargar_resenias(self):
        if 'lista_resenias' in self.ids:
            self.ids.lista_resenias.clear_widgets()

        UrlRequest(
            f"{BASE_URL}/resenias",
            on_success=self.resenias_cargadas_ok,
            on_failure=self.error_carga,
            on_error=self.error_carga
        )

    def resenias_cargadas_ok(self, req, result):
        if 'lista_resenias' not in self.ids:
            return
        
        self.cargar_reservas()

        self.ids.puntuacion.values = [str(i) for i in range(1,6)]

        self.cargar_platos()

        if not result:
            self.ids.lista_resenias.add_widget(Label(text="No has dejado reseñas aún.", size_hint_y=None, height=40))
            return

        resenias = result

        for resenia in resenias:
            plato = resenia.get('nombre_plato') if isinstance(resenia, dict) else resenia[2]
            comentario = resenia.get('comentario') if isinstance(resenia, dict) else resenia[3]

            texto_resenia = f"{plato} - {comentario}"
            
            item = Factory.ReseniaItem()
            item.texto = texto_resenia

            self.ids.lista_resenias.add_widget(item)
            
    def error_carga(self, req, error):
        if 'lista_resenias' in self.ids:
            self.ids.lista_resenias.add_widget(Label(text="Error al cargar tus resenias. (ERROR BACKEND)", color=[1,0,0,1], size_hint_y=None, height=40))



class PrincipalScreen(Screen):
    def ir_a_reservas(self):
        self.manager.current = 'reservas'
        self.manager.get_screen('reservas').cargar_reservas()
    
    def ir_a_resenias(self):
        self.manager.current = 'resenias'
        self.manager.get_screen('resenias').cargar_resenias()

    def ir_a_carta_publica(self):
        self.manager.current = 'carta'
        self.manager.get_screen('carta').cargar_platos()

    def cerrar_sesion(self):
        self.manager.current = 'inicio'



class RestoApp(App):
    def build(self):
        
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_kv = os.path.join(directorio_actual, 'main.kv')
        
       
        try:
            Builder.unload_file(ruta_kv)
        except:
            pass
            
      
        return Builder.load_file(ruta_kv)


if __name__ == '__main__':
    RestoApp().run()