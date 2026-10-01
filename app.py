"""Ponto de entrada Flask. Rotas apenas renderizam; sem regra tributária aqui."""
from flask import Flask, render_template, request

from src.models.tax import SimulationStatus
from src.services import simulate
from src.services.guided_simulation import ENQUADRAMENTO_LABELS, simulate_guided, rotulo_ramo
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
    width,
    humanize,
    pct,
)
from src.services.simulation_input_adapter import SimulationInputError, build_guided_input, build_scenario
from src.tax_rules import SUPPORTED_YEARS, load_year_rules

PAGES = {
    "index": ("/", "index.html"),
    "simulation": ("/simulacao", "simulation.html"),
    "pf": ("/simulacao/pf", "pf.html"),
    "mei": ("/simulacao/mei", "mei.html"),
    "simples": ("/simulacao/simples", "simples.html"),
    "compare": ("/simulacao/comparar", "compare.html"),
    "result": ("/resultado", "result.html"),
    "about": ("/sobre", "about.html"),
    "mind_map": ("/mapa-mental", "mind_map.html"),
}
# Etapas da linha do tempo educacional da reforma (rótulo, exercícios cujos arquivos de regras são contados)
REFORM_STAGES = (
    ("2026", (2026,)), ("2027–2028", (2027, 2028)), ("2029", (2029,)), ("2030", (2030,)),
    ("2031", (2031,)), ("2032", (2032,)), ("2033", (2033,)),
)
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
        width=width, label_enq=ENQUADRAMENTO_LABELS.get, label_limite=LIMITE_LABELS.get, label_anexo=ANEXO_LABELS.get, label_status=STATUS_LABELS.get,
    )
    app.jinja_env.globals.update(OK=SimulationStatus.OK)

    for endpoint, (path, template) in PAGES.items():
        app.add_url_rule(path, endpoint, lambda t=template: render_template(t))

    @app.get("/reforma")
    def reform():
        etapas = []
        for rotulo, anos in REFORM_STAGES:
            regras = [r for ano in anos for r in load_year_rules(ano)["regras"]]
            testadas = sum(1 for r in regras if r.get("status") == "TESTADA")
            etapas.append({
                "rotulo": rotulo,
                "slug": rotulo.replace("–", "-"),
                "regras": len(regras),
                "testadas": testadas,
                "implementado": testadas > 0,
            })
        return render_template("reform.html", etapas=etapas)

    @app.get("/simulacao-guiada")
    def guided():
        return render_template("guided_simulation.html")

    @app.post("/simulacao-guiada")
    def guided_result():
        try:
            entrada = build_guided_input(request.form)
        except SimulationInputError as exc:
            return render_template(
                "guided_simulation.html", form=request.form, errors=exc.errors, general=exc.general
            ), 422
        return render_template(
            "guided_simulation_result.html", g=simulate_guided(entrada), ramo=rotulo_ramo(entrada)
        )

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
