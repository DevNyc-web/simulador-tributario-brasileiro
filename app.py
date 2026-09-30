"""Ponto de entrada Flask. Rotas apenas renderizam; sem regra tributária aqui."""
from flask import Flask, render_template, request

from src.models.tax import SimulationStatus
from src.services import simulate
from src.services.presentation import (
    ANEXO_LABELS,
    ATIVIDADE_LABELS,
    CATEGORIA_LABELS,
    LIMITE_LABELS,
    MODO_LABELS,
    PLANO_LABELS,
    STATUS_LABELS,
    brl,
    choices,
    decimal_br,
    humanize,
    pct,
)
from src.services.simulation_input_adapter import SimulationInputError, build_scenario
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
    "mind_map": ("/mapa-mental", "mind_map.html"),
}
FORM_TEMPLATES = {"pf": "pf.html", "mei": "mei.html", "simples": "simples.html", "comparar": "compare.html"}


def create_app() -> Flask:
    app = Flask(__name__)

    @app.context_processor
    def shared_context() -> dict:
        return {"years": list(SUPPORTED_YEARS), "choices": choices(), "form": {}, "errors": {}, "general": []}

    app.jinja_env.filters.update(
        brl=brl, pct=pct, decimal_br=decimal_br, humanize=humanize,
        label_plano=PLANO_LABELS.get, label_categoria=CATEGORIA_LABELS.get,
        label_atividade=ATIVIDADE_LABELS.get, label_modo=MODO_LABELS.get,
        label_limite=LIMITE_LABELS.get, label_anexo=ANEXO_LABELS.get, label_status=STATUS_LABELS.get,
    )
    app.jinja_env.globals.update(OK=SimulationStatus.OK)

    for endpoint, (path, template) in PAGES.items():
        app.add_url_rule(path, endpoint, lambda t=template: render_template(t))

    @app.post("/resultado")
    def result_post():
        form = request.form
        try:
            scenario = build_scenario(form)
        except SimulationInputError as exc:
            template = FORM_TEMPLATES.get(form.get("tipo_simulacao", ""))
            if template is None:
                return render_template("simulation.html", general=exc.general), 400
            return render_template(template, form=form, errors=exc.errors, general=exc.general), 422
        return render_template("result.html", outcome=simulate(scenario))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
