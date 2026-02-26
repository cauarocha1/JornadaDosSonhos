from pathlib import Path
from unittest.mock import patch

import requests

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

import sys

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from jornada_core import (  # noqa: E402
    compute_scenarios,
    detect_help_intent,
    detect_list_goals_intent,
    detect_new_goal_intent,
    detect_out_of_scope,
    detect_restart_intent,
    feasible_feedback,
    ollama_generate,
    parse_currency,
    parse_months,
    prettify_dream_name,
)


def run():
    results = []

    # Cenario 1: simulacao viavel
    c1 = compute_scenarios(35000.0, 5000.0, 24)
    ok1 = c1["conservador"]["aporte"] > c1["moderado"]["aporte"] > 0
    results.append(("Cenario 1 - Simulacao viavel", ok1, c1))

    # Cenario 2: alerta de inviabilidade
    c2 = compute_scenarios(1_000_000.0, 0.0, 12)
    warning = feasible_feedback(c2["moderado"]["aporte"], 2000.0, 1_000_000.0, 0.0)
    ok2 = warning is not None and "consumiria" in warning
    results.append(("Cenario 2 - Alerta inviavel", ok2, warning))

    # Cenario 3: parse basico
    ok3 = parse_currency("R$ 35.000") == 35000.0 and parse_months("2 anos") == 24
    results.append(("Cenario 3 - Parse dados", ok3, "currency+months"))

    # Cenario 4: fallback sem Ollama
    with patch("jornada_core.requests.post", side_effect=requests.RequestException("offline")):
        llm = ollama_generate("teste")
    ok4 = llm == ""
    results.append(("Cenario 4 - Fallback Ollama", ok4, llm))

    # Cenario 5: bloqueio fora de escopo
    block = detect_out_of_scope("O santos joga amanha?")
    ok5 = block is not None and "financas pessoais" in block
    results.append(("Cenario 5 - Escopo", ok5, block))

    # Cenario 6: formatacao de sonho
    dream = prettify_dream_name("Eu quero passar duas semanas no japao?")
    ok6 = dream == "Viagem no Japao"
    results.append(("Cenario 6 - Formatar sonho", ok6, dream))

    # Cenario 7: intencoes
    ok7 = (
        detect_help_intent("como funciona esta aplicacao?")
        and detect_list_goals_intent("quero ver minhas metas")
        and detect_new_goal_intent("quero criar nova meta")
        and detect_restart_intent("vamos reiniciar")
    )
    results.append(("Cenario 7 - Intencoes", ok7, "help/list/new/restart"))

    approved = all(item[1] for item in results)
    for name, ok, detail in results:
        status = "APROVADO" if ok else "REPROVADO"
        print(f"{name}: {status}")
        print(f"  detalhe: {detail}")

    print("-" * 60)
    print(f"Resultado final: {'APROVADO' if approved else 'REPROVADO'}")
    return 0 if approved else 1


if __name__ == "__main__":
    raise SystemExit(run())
