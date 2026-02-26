import json
import re
import unicodedata
from pathlib import Path

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

ESTIMATIVAS_SONHOS = {
    "intercambio": {
        "keywords": ["intercambio", "dublin", "curso no exterior"],
        "faixa": [30000.0, 45000.0],
        "observacao": "estimativa para 6 meses com estudo e custo de vida",
    },
    "viagem_internacional": {
        "keywords": ["viagem", "europa", "japao", "canada"],
        "faixa": [18000.0, 35000.0],
        "observacao": "estimativa para 2 a 3 semanas, sem luxo",
    },
    "casamento": {
        "keywords": ["casamento", "festa", "cerimonia"],
        "faixa": [35000.0, 90000.0],
        "observacao": "estimativa para evento de porte medio",
    },
    "carro": {
        "keywords": ["carro", "automovel", "veiculo"],
        "faixa": [55000.0, 130000.0],
        "observacao": "estimativa para compra de carro de entrada a intermediario",
    },
    "entrada_imovel": {
        "keywords": ["apartamento", "imovel", "casa", "entrada"],
        "faixa": [50000.0, 180000.0],
        "observacao": "estimativa para entrada de imovel em grandes centros",
    },
}

OFF_TOPIC_KEYWORDS = [
    "clima",
    "tempo",
    "temperatura",
    "chuva",
    "sol",
    "previsao",
    "futebol",
    "jogo",
    "resultado",
    "placar",
    "campeonato",
    "gol",
    "partida",
    "time",
    "filme",
    "serie",
    "receita",
    "cozinha",
    "musica",
]
OFF_TOPIC_KEYWORDS_NORMALIZED = [
    unicodedata.normalize("NFKD", k).encode("ascii", "ignore").decode("ascii").lower()
    for k in OFF_TOPIC_KEYWORDS
]

SCOPE_BLOCK_MESSAGE = (
    "Eu so respondo assuntos de financas pessoais e planejamento de metas. "
    "Posso te ajudar com orcamento, poupanca, investimentos de forma educativa e simulacao de metas."
)

SYSTEM_PROMPT_JORNADA = """Voce e a Jornada, uma planejadora financeira amigavel e didatica.

OBJETIVO:
Transformar sonhos em metas matematicas de forma simples e segura.

REGRAS:
- NUNCA recomende investimentos especificos como ordem de compra;
- NUNCA prometa rendimento futuro;
- JAMAIS responda perguntas fora de financas pessoais;
- Se nao souber algo, admita com transparencia e ofereca explicacao educativa;
- Sempre mantenha linguagem simples, direta e sem jargao desnecessario;
- Sempre pergunte no final se a pessoa quer ajustar prazo, valor-meta ou aporte;
- Responda em no maximo 3 paragrafos curtos.
"""


def _normalize_text(text: str):
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return ascii_text.lower()


def detect_out_of_scope(text: str):
    if not text:
        return None
    normalized = _normalize_text(text)
    if any(keyword in normalized for keyword in OFF_TOPIC_KEYWORDS_NORMALIZED):
        return SCOPE_BLOCK_MESSAGE
    return None


def load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return fallback


def save_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def parse_currency(text: str):
    if not text:
        return None
    raw = text.lower().replace("r$", "").replace(" ", "")
    if "," in raw and "." in raw:
        raw = raw.replace(".", "").replace(",", ".")
    else:
        raw = raw.replace(",", ".")
    match = re.search(r"-?\d+(?:\.\d+)?", raw)
    if not match:
        return None
    value = float(match.group())
    return value if value >= 0 else None


def parse_months(text: str):
    if not text:
        return None
    base = _normalize_text(text)
    years = re.search(r"(\d+)\s*(ano|anos)", base)
    months = re.search(r"(\d+)\s*(mes|meses)", base)
    if years:
        return int(years.group(1)) * 12
    if months:
        return int(months.group(1))
    numeric = re.search(r"\d+", base)
    if numeric:
        return int(numeric.group())
    return None


def estimate_goal_by_keywords(dream: str):
    text = _normalize_text(dream)
    for item in ESTIMATIVAS_SONHOS.values():
        if any(keyword in text for keyword in item["keywords"]):
            return item["faixa"], item["observacao"]
    return (15000.0, 50000.0), "faixa generica para metas de medio porte"


def pmt_for_goal(goal_value: float, initial_amount: float, months: int, monthly_rate: float):
    future_initial = initial_amount * ((1 + monthly_rate) ** months)
    remaining = goal_value - future_initial
    if remaining <= 0:
        return 0.0
    factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    return remaining / factor


def compute_scenarios(goal_value: float, initial_amount: float, months: int):
    conservative = pmt_for_goal(goal_value, initial_amount, months, 0.005)
    moderate = pmt_for_goal(goal_value, initial_amount, months, 0.008)
    return {
        "conservador": {"taxa": 0.005, "aporte": round(conservative, 2)},
        "moderado": {"taxa": 0.008, "aporte": round(moderate, 2)},
    }


def months_for_budget(goal_value: float, initial_amount: float, budget: float, monthly_rate: float):
    if budget <= 0:
        return None
    for m in range(1, 721):
        required = pmt_for_goal(goal_value, initial_amount, m, monthly_rate)
        if required <= budget:
            return m
    return None


def feasible_feedback(aporte: float, renda_mensal: float, goal_value: float, initial_amount: float):
    if not renda_mensal or renda_mensal <= 0:
        return None
    ratio = aporte / renda_mensal
    if ratio < 0.8:
        return None

    budget = renda_mensal * 0.35
    suggested_months = months_for_budget(goal_value, initial_amount, budget, 0.008)
    if suggested_months:
        return (
            f"Guardar R$ {aporte:,.2f} por mes consumiria {ratio:.0%} da sua renda. "
            f"Para uma jornada viavel, podemos mirar cerca de R$ {budget:,.2f}/mes e estender para "
            f"{suggested_months} meses."
        )

    return (
        f"Guardar R$ {aporte:,.2f} por mes consumiria {ratio:.0%} da sua renda. "
        "Mesmo alongando bastante o prazo, a meta ainda ficaria agressiva. "
        "Podemos reduzir o valor-alvo ou dividir a meta em fases."
    )


def format_currency(value: float):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ollama_generate(prompt: str):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODELO, "prompt": prompt, "stream": False},
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("response", "").strip()
    except (requests.RequestException, ValueError, KeyError):
        return ""


def empathetic_wrap(core_text: str, dream_name: str, user_context: str = ""):
    style_prompt = f"""
{SYSTEM_PROMPT_JORNADA}

CONTEXTO DO CLIENTE:
- sonho: {dream_name}
{user_context}

INSTRUCAO:
Reescreva a mensagem base preservando todos os numeros e limites.
Se faltar informacao, admita com clareza.

MENSAGEM BASE:
{core_text}
"""
    llm_text = ollama_generate(style_prompt)
    return llm_text if llm_text else core_text
