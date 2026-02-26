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
<<<<<<< HEAD
    detect_help_intent,
    detect_list_goals_intent,
    detect_new_goal_intent,
    detect_out_of_scope,
    detect_restart_intent,
=======
    detect_out_of_scope,
    empathetic_wrap,
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
    feasible_feedback,
    ollama_generate,
    parse_currency,
    parse_months,
<<<<<<< HEAD
    prettify_dream_name,
=======
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
)


def run():
    results = []

<<<<<<< HEAD
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
=======
    # Cenário 1: meta viável
    c1 = compute_scenarios(35000.0, 5000.0, 24)
    ok1 = c1["conservador"]["aporte"] > c1["moderado"]["aporte"] > 0
    results.append(("Cenário 1 - Meta viável", ok1, c1))

    # Cenário 2: meta inviável para renda
    c2 = compute_scenarios(1_000_000.0, 0.0, 12)
    warning = feasible_feedback(c2["moderado"]["aporte"], 2000.0, 1_000_000.0, 0.0)
    ok2 = warning is not None and "consumiria" in warning
    results.append(("Cenário 2 - Meta inviável", ok2, warning))

    # Cenário 3: entradas inválidas
    ok3 = parse_currency("texto solto") is None and parse_months("depois") is None
    results.append(("Cenário 3 - Entrada inválida", ok3, "parse inválido tratado"))

    # Cenário 4: fallback sem Ollama
    with patch("jornada_core.requests.post", side_effect=requests.RequestException("offline")):
        llm = ollama_generate("teste")
        wrapped = empathetic_wrap("mensagem base", "Intercâmbio")
    ok4 = llm == "" and wrapped == "mensagem base"
    results.append(("Cenário 4 - Fallback sem Ollama", ok4, wrapped))

    # Cenário 5: pergunta fora de finanças
    block_msg = detect_out_of_scope("Qual o clima de hoje?")
    ok5 = block_msg is not None and "respondo assuntos de financas" in block_msg
    results.append(("Cenário 5 - Bloqueio fora de escopo", ok5, block_msg))
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0

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
