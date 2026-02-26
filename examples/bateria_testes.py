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
    detect_out_of_scope,
    empathetic_wrap,
    feasible_feedback,
    ollama_generate,
    parse_currency,
    parse_months,
)


def run():
    results = []

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
