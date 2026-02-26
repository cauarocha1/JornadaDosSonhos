<<<<<<< HEAD
import csv
=======
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
import json
import re
import unicodedata
from pathlib import Path

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

<<<<<<< HEAD
SCOPE_BLOCK_MESSAGE = (
    "Eu so respondo assuntos de financas pessoais e planejamento de metas. "
    "Posso te ajudar com sonhos, metas, simulacoes e organizacao financeira."
)

OFF_TOPIC_PATTERNS = [
    "previsao do tempo",
    "qual o clima",
    "vai chover",
    "temperatura",
    "resultado do jogo",
    "placar",
    "campeonato",
    "rodada",
    "partida",
    "filme",
    "serie",
    "receita culinaria",
]

TEAM_KEYWORDS = [
    "santos",
    "flamengo",
    "palmeiras",
    "corinthians",
    "sao paulo",
    "vasco",
    "gremio",
    "internacional",
    "botafogo",
    "atletico",
    "cruzeiro",
]


def normalize_text(text: str):
    normalized = unicodedata.normalize("NFKD", text or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", ascii_text).strip().lower()
=======
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
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0


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
<<<<<<< HEAD
    raw = normalize_text(text).replace("r$", "").replace(" ", "")
    if "," in raw and "." in raw:
        raw = raw.replace(".", "").replace(",", ".")
    elif "," in raw:
        raw = raw.replace(",", ".")
    else:
        if raw.count(".") > 1:
            raw = raw.replace(".", "")
        elif raw.count(".") == 1:
            left, right = raw.split(".", 1)
            # Heuristica BR: "35.000" -> 35000
            if len(right) == 3 and left.isdigit() and right.isdigit():
                raw = left + right
=======
    raw = text.lower().replace("r$", "").replace(" ", "")
    if "," in raw and "." in raw:
        raw = raw.replace(".", "").replace(",", ".")
    else:
        raw = raw.replace(",", ".")
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
    match = re.search(r"-?\d+(?:\.\d+)?", raw)
    if not match:
        return None
    value = float(match.group())
    return value if value >= 0 else None


def parse_months(text: str):
    if not text:
        return None
<<<<<<< HEAD
    base = normalize_text(text)
=======
    base = _normalize_text(text)
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
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


<<<<<<< HEAD
def format_currency(value: float):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def configure_ollama(url: str | None = None, model: str | None = None):
    global OLLAMA_URL, MODELO
    if url:
        OLLAMA_URL = url.rstrip("/")
    if model:
        MODELO = model.strip()


def ollama_health():
    base_url = OLLAMA_URL.replace("/api/generate", "")
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        response.raise_for_status()
        payload = response.json()
        models = [m.get("name", "") for m in payload.get("models", []) if m.get("name")]
        return True, models
    except (requests.RequestException, ValueError):
        return False, []


def ollama_generate(prompt: str):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODELO, "prompt": prompt, "stream": False},
            timeout=25,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("response", "").strip()
    except (requests.RequestException, ValueError, KeyError):
        return ""


def extract_system_prompt(markdown_text: str):
    match = re.search(r"```text\s*(.*?)```", markdown_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return (
        "Voce e a Jornada, agente de planejamento financeiro por metas. "
        "Nao recomende ativos especificos e nao responda fora de financas."
    )


def detect_out_of_scope(text: str):
    normalized = normalize_text(text)
    if not normalized:
        return None

    if any(pattern in normalized for pattern in OFF_TOPIC_PATTERNS):
        return SCOPE_BLOCK_MESSAGE

    sports_terms = ["jogo", "joga", "placar", "resultado", "rodada", "gol", "campeonato"]
    if any(term in normalized for term in sports_terms) and any(team in normalized for team in TEAM_KEYWORDS):
        return SCOPE_BLOCK_MESSAGE

    if "clima" in normalized or "tempo amanha" in normalized or "tempo hoje" in normalized:
        return SCOPE_BLOCK_MESSAGE

    return None


def detect_help_intent(text: str):
    normalized = normalize_text(text)
    help_terms = [
        "como funciona",
        "como usar",
        "o que voce faz",
        "explica a aplicacao",
        "explica o app",
        "ajuda",
    ]
    return any(term in normalized for term in help_terms)


def detect_list_goals_intent(text: str):
    normalized = normalize_text(text)
    terms = ["listar metas", "minhas metas", "ver metas", "consultar metas", "mostrar metas"]
    return any(term in normalized for term in terms)


def detect_goal_detail_intent(text: str):
    normalized = normalize_text(text)
    if "meta" not in normalized:
        return None
    match = re.search(r"meta\s*(\d+)", normalized)
    if match:
        return int(match.group(1))
    return None


def detect_new_goal_intent(text: str):
    normalized = normalize_text(text)
    terms = [
        "nova meta",
        "novo plano",
        "criar meta",
        "adicionar meta",
        "mais uma meta",
        "outra meta",
        "quero",
        "sonho",
    ]
    return any(term in normalized for term in terms)


def detect_restart_intent(text: str):
    normalized = normalize_text(text)
    terms = [
        "reiniciar",
        "recomecar",
        "comecar de novo",
        "outro plano",
        "novo plano",
        "resetar",
        "reset",
    ]
    return any(term in normalized for term in terms)


def prettify_dream_name(text: str):
    normalized = normalize_text(text).strip(" ?!.")
    if not normalized:
        return "Meta Financeira"

    predefined = [
        ("japao", "Viagem no Japao"),
        ("dublin", "Intercambio em Dublin"),
        ("intercambio", "Intercambio Internacional"),
        ("casamento", "Casamento"),
        ("apartamento", "Entrada de Apartamento"),
        ("imovel", "Entrada de Imovel"),
        ("casa", "Entrada de Casa"),
        ("carro", "Compra de Carro"),
        ("viagem", "Viagem Internacional"),
    ]
    for keyword, label in predefined:
        if keyword in normalized:
            return label

    normalized = re.sub(
        r"^(eu quero|quero|gostaria de|meu sonho e|meu sonho eh|sonho de|eu gostaria de)\s+",
        "",
        normalized,
    )
    normalized = re.sub(r"^(passar|fazer|ter|comprar|juntar)\s+", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    if not normalized:
        return "Meta Financeira"

    stop_words = {"de", "do", "da", "dos", "das", "e", "em", "no", "na", "para", "por"}
    words = []
    for index, word in enumerate(normalized.split(" ")[:7]):
        if index > 0 and word in stop_words:
            words.append(word)
        else:
            words.append(word.capitalize())
    return " ".join(words)


def estimate_goal_by_keywords(dream_name: str):
    normalized = normalize_text(dream_name)
    table = [
        (["intercambio", "dublin"], (30000.0, 45000.0), "estimativa para 6 meses"),
        (["japao", "viagem", "europa", "canada"], (18000.0, 35000.0), "estimativa para 2 a 3 semanas"),
        (["casamento"], (35000.0, 90000.0), "estimativa para evento medio"),
        (["carro"], (55000.0, 130000.0), "estimativa para compra de carro"),
        (["apartamento", "imovel", "casa", "entrada"], (50000.0, 180000.0), "estimativa para entrada"),
    ]
    for keywords, faixa, obs in table:
        if any(keyword in normalized for keyword in keywords):
            return faixa, obs
=======
def estimate_goal_by_keywords(dream: str):
    text = _normalize_text(dream)
    for item in ESTIMATIVAS_SONHOS.values():
        if any(keyword in text for keyword in item["keywords"]):
            return item["faixa"], item["observacao"]
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
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
<<<<<<< HEAD
    for month in range(1, 721):
        required = pmt_for_goal(goal_value, initial_amount, month, monthly_rate)
        if required <= budget:
            return month
=======
    for m in range(1, 721):
        required = pmt_for_goal(goal_value, initial_amount, m, monthly_rate)
        if required <= budget:
            return m
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
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
<<<<<<< HEAD
            f"Guardar {format_currency(aporte)} por mes consumiria {ratio:.0%} da sua renda. "
            f"Para manter viabilidade, podemos mirar {format_currency(budget)}/mes e prazo de {suggested_months} meses."
        )

    return (
        f"Guardar {format_currency(aporte)} por mes consumiria {ratio:.0%} da sua renda. "
        "Mesmo com prazo longo, a meta fica agressiva. Podemos reduzir valor-alvo ou dividir em fases."
    )


def summarize_transactions(csv_path: Path, max_rows: int = 8):
    if not csv_path.exists():
        return "Sem transacoes."
    rows = []
    try:
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                if idx >= max_rows:
                    break
                rows.append(
                    f"- {row.get('data','')}: {row.get('descricao','')} "
                    f"({row.get('categoria','')}) {row.get('tipo','')} {row.get('valor','')}"
                )
    except OSError:
        return "Sem transacoes."
    return "\n".join(rows) if rows else "Sem transacoes."


def summarize_history(csv_path: Path, max_rows: int = 5):
    if not csv_path.exists():
        return "Sem historico."
    rows = []
    try:
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                if idx >= max_rows:
                    break
                rows.append(f"- {row.get('data','')}: {row.get('tema','')} - {row.get('resumo','')}")
    except OSError:
        return "Sem historico."
    return "\n".join(rows) if rows else "Sem historico."


def build_knowledge_context(data_dir: Path):
    profile = load_json(data_dir / "perfil_investidor.json", {})
    products = load_json(data_dir / "produtos_financeiros.json", [])
    profile_summary = (
        f"Cliente base: {profile.get('nome','N/A')}, renda {profile.get('renda_mensal','N/A')}, "
        f"perfil {profile.get('perfil_investidor','N/A')}, objetivo {profile.get('objetivo_principal','N/A')}."
    )

    product_lines = []
    if isinstance(products, list):
        for item in products[:5]:
            name = item.get("nome", "N/A")
            desc = item.get("descricao") or item.get("uso_no_app") or item.get("categoria", "")
            product_lines.append(f"- {name}: {desc}")
    products_summary = "\n".join(product_lines) if product_lines else "- Sem produtos/cenarios cadastrados."

    transactions_summary = summarize_transactions(data_dir / "transacoes.csv")
    history_summary = summarize_history(data_dir / "historico_atendimento.csv")

    return (
        "BASE DE CONHECIMENTO\n"
        f"{profile_summary}\n\n"
        "Transacoes recentes:\n"
        f"{transactions_summary}\n\n"
        "Historico de atendimento:\n"
        f"{history_summary}\n\n"
        "Cenarios e regras:\n"
        f"{products_summary}"
    )


def build_goals_context(goals: list[dict]):
    if not goals:
        return "Usuario ainda sem metas."
    lines = []
    for item in goals[:10]:
        lines.append(
            f"- Meta {item.get('id_meta')}: {item.get('nome_sonho')} | "
            f"valor {item.get('valor_meta')} | prazo {item.get('prazo_meses')} meses | status {item.get('status')}"
        )
    return "\n".join(lines)


def format_chat_history(messages: list[dict], max_messages: int = 10):
    tail = messages[-max_messages:]
    lines = []
    for item in tail:
        role = item.get("role", "user")
        content = item.get("content", "")
        lines.append(f"{role.upper()}: {content}")
    return "\n".join(lines)


def build_agent_prompt(
    system_prompt: str,
    docs_context: str,
    knowledge_context: str,
    goals_context: str,
    chat_history: str,
    user_message: str,
):
    return f"""
{system_prompt}

CONTEXTO DE DOCUMENTACAO:
{docs_context}

{knowledge_context}

METAS DO USUARIO:
{goals_context}

HISTORICO DA CONVERSA:
{chat_history}

MENSAGEM DO USUARIO:
{user_message}

INSTRUCOES FINAIS:
- Responda em portugues do Brasil.
- Seja objetiva e util.
- Se usuario perguntar como funciona, explique em passos simples.
- Se usuario pedir recomendacao de ativo, recuse e ofereca simulacao de meta.
- Se faltar dado para simulacao, peça os dados faltantes.
"""


def generate_agent_reply(
    user_message: str,
    system_prompt: str,
    docs_context: str,
    knowledge_context: str,
    goals_context: str,
    messages: list[dict],
):
    prompt = build_agent_prompt(
        system_prompt=system_prompt,
        docs_context=docs_context,
        knowledge_context=knowledge_context,
        goals_context=goals_context,
        chat_history=format_chat_history(messages),
        user_message=user_message,
    )
    return ollama_generate(prompt)
=======
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
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
