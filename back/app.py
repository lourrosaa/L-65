from flask import Flask
from flask_cors import CORS

from routes.carta import carta_bp
from routes.registro_usuarios import registro_usuarios_bp
from routes.reservas import reservas_bp
from routes.reseñas import reseñas_bp
from routes.platos_populares import platos_populares_bp
from routes.admin import admin_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(carta_bp)
app.register_blueprint(registro_usuarios_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(reseñas_bp)
app.register_blueprint(platos_populares_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)