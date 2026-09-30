"""Ponto de entrada Flask. Rotas apenas renderizam; sem regra tributária aqui."""
from flask import Flask, render_template

from src.tax_rules import SUPPORTED_YEARS

PAGES = {
    "index": ("/", "index.html"),
    "simulation": ("/simulacao", "simulation.html"),
    "pf": ("/simulacao/pf", "pf.html"),
    "mei": ("/simulacao/mei", "mei.html"),
    "simples": ("/simulacao/simples", "simples.html"),
    "compare": ("/simulacao/comparar", "compare.html"),
    "result": ("/resultado", "result.html"),
    "reform": ("/reforma", "reform.html"),
    "about": ("/sobre", "about.html"),
}


def create_app() -> Flask:
    app = Flask(__name__)

    @app.context_processor
    def shared_context() -> dict:
        return {"years": list(SUPPORTED_YEARS)}

    for endpoint, (path, template) in PAGES.items():
        app.add_url_rule(
            path, endpoint, lambda t=template: render_template(t)
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
