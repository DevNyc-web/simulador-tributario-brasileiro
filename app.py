"""Ponto de entrada Flask. Rotas apenas renderizam; sem regra tributária aqui."""
from flask import Flask, render_template

from src.services import simulate_transition

PROFILES = ["Pessoa Física", "MEI", "Simples Nacional", "Lucro Presumido", "Reforma Tributária"]


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html", profiles=PROFILES)

    @app.route("/simulacao")
    def simulation():
        return render_template("simulation.html", results=simulate_transition({}))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
