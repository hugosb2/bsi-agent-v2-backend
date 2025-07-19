from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    from .controllers.agent_controller import agent_bp
    
    app.register_blueprint(agent_bp)

    @app.route("/")
    def index():
        return "Servidor do Agente de IA está no ar!"

    return app
