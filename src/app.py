import json
import re
import unicodedata
from pathlib import Path

import requests
import streamlit as st

# Config
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"

DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gpt-oss"
DEFAULT_CONNECT_TIMEOUT = 8
DEFAULT_READ_TIMEOUT = 240
DEFAULT_HEALTH_TIMEOUT = 6


def normalize_ollama_generate_url(url: str) -> str:
    base = (url or "").strip().rstrip("/")
    if not base:
        return DEFAULT_OLLAMA_URL
    if base.endswith("/api/generate"):
        return base
    if "/api/" in base:
        return base
    return f"{base}/api/generate"


def candidate_generate_urls(url: str) -> list[str]:
    primary = normalize_ollama_generate_url(url)
    alt = primary.replace("localhost", "127.0.0.1")
    return [primary] if alt == primary else [primary, alt]


def load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def extract_system_prompt_from_docs() -> str:
    prompt_file = DOCS_DIR / "03-prompts.md"
    if not prompt_file.exists():
        return "Voce e a Jornada, planejadora financeira focada em metas."
    content = prompt_file.read_text(encoding="utf-8")
    match = re.search(r"```text\s*(.*?)```", content, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return content.strip()


def build_knowledge_context() -> str:
    perfil = load_json(DATA_DIR / "perfil_investidor.json", {})
    produtos = load_json(DATA_DIR / "produtos_financeiros.json", [])
    jornada = load_json(DATA_DIR / "jornada_contexto.json", {})
    transacoes_txt = read_text(DATA_DIR / "transacoes.csv")
    historico_txt = read_text(DATA_DIR / "historico_atendimento.csv")

    parts = [
        "DADOS_DE_PERFIL:\n" + (json.dumps(perfil, ensure_ascii=False, indent=2) if perfil else "{}"),
        "TRANSACOES:\n" + (transacoes_txt or "Sem transacoes."),
        "HISTORICO:\n" + (historico_txt or "Sem historico."),
        "PRODUTOS:\n" + (json.dumps(produtos, ensure_ascii=False, indent=2) if produtos else "[]"),
        "JORNADA_CONTEXTO:\n" + (json.dumps(jornada, ensure_ascii=False, indent=2) if jornada else "{}"),
    ]
    return "\n\n".join(parts)


def build_prompt(system_prompt: str, contexto: str, historico: str, pergunta: str) -> str:
    return (
        f"{system_prompt}\n\n"
        f"CONTEXT:{contexto}\n\n"
        f"HISTORICO:{historico}\n\n"
        f"PERGUNTA:{pergunta}\n\n"
        "Responda em portugues do Brasil, seja direto e util. "
        "Use valores monetarios no formato R$ 9.999,99."
    )


def normalize_ai_text(text: str) -> str:
    if not text:
        return ""
    t = unicodedata.normalize("NFKC", text)

    # Remove caracteres invisiveis que baguncam renderizacao.
    t = re.sub(r"[\u200B-\u200F\u2060\uFEFF]", "", t)
    t = t.replace("\u00A0", " ").replace("\u202F", " ").replace("\u2007", " ")

    # Uniformiza hifens especiais.
    t = re.sub(r"[\u2010-\u2015]", "-", t)

    # Corrige "R 2300" ou "R2300" para "R$ 2300".
    t = re.sub(r"(?<!\w)R\s*(?=\d)", "R$ ", t)

    # Junta palavras quebradas letra-a-letra: "m e n s a l" -> "mensal".
    def _join_spelled(match: re.Match) -> str:
        return re.sub(r"\s+", "", match.group(0))

    t = re.sub(r"\b(?:[A-Za-zÀ-ÿ]\s+){3,}[A-Za-zÀ-ÿ]\b", _join_spelled, t)

    # Compacta espacos/quebras excessivos.
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"\s+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def ollama_health(url: str) -> tuple[bool, list]:
    try:
        base = candidate_generate_urls(url)[0]
        base = base[: -len("/api/generate")] if base.endswith("/api/generate") else base
        r = requests.get(f"{base}/api/tags", timeout=DEFAULT_HEALTH_TIMEOUT)
        r.raise_for_status()
        payload = r.json()
        models = [m.get("name") for m in payload.get("models", []) if m.get("name")]
        return True, models
    except Exception:
        return False, []


def resolve_model(modelo: str, models: list[str]) -> str:
    if not models:
        return modelo
    if modelo in models:
        return modelo
    for m in models:
        if m.split(":")[0] == modelo:
            return m
    return models[0]


def ask_ollama(
    prompt: str,
    ollama_url: str,
    modelo: str,
    models_online: list[str],
    connect_timeout: int = DEFAULT_CONNECT_TIMEOUT,
    read_timeout: int = DEFAULT_READ_TIMEOUT,
) -> str:
    urls = candidate_generate_urls(ollama_url)
    chosen = resolve_model(modelo, models_online)

    def _call(u: str):
        r = requests.post(
            u,
            json={
                "model": chosen,
                "prompt": prompt,
                "stream": False,
                "keep_alive": "30m",
            },
            timeout=(connect_timeout, read_timeout),
        )
        r.raise_for_status()
        return r.json()

    errors = []
    for idx, url in enumerate(urls):
        try:
            data = _call(url)
            raw = str(data.get("response", "")).strip() or ""
            return normalize_ai_text(raw)
        except requests.exceptions.Timeout:
            errors.append(f"timeout em {url}")
        except Exception as e:
            errors.append(f"falha em {url}: {e}")

        # Usa timeout maior na segunda tentativa para absorver cold start do modelo.
        if idx == 0 and len(urls) > 1:
            read_timeout = max(read_timeout, DEFAULT_READ_TIMEOUT)

    detail = " | ".join(errors) if errors else "falha desconhecida"
    return (
        "Erro ao conectar ao motor de IA. "
        "Confirme se o Ollama esta ativo e se o modelo foi baixado (ollama pull). "
        f"Detalhe: {detail}"
    )


# ---------- Interface Streamlit ----------
st.set_page_config(page_title="Jornada - Agente IA", page_icon="🎯", layout="centered")
st.title("🎯 Jornada - Agente de IA")

st.sidebar.header("Ollama")
ollama_url = st.sidebar.text_input("URL API", value=DEFAULT_OLLAMA_URL)
modelo = st.sidebar.text_input("Modelo", value=DEFAULT_MODEL)
read_timeout = st.sidebar.slider("Timeout de leitura (s)", min_value=60, max_value=600, value=DEFAULT_READ_TIMEOUT, step=30)

online, models = ollama_health(ollama_url)
if online:
    st.sidebar.success("Ollama conectado")
    if models:
        st.sidebar.caption("Modelos: " + ", ".join(models))
else:
    st.sidebar.warning("Ollama indisponivel")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Oi — sou a Jornada. Vamos transformar seu sonho em uma meta financeira."}
    ]

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if user_msg := st.chat_input("Converse com a Jornada..."):
    st.session_state.messages.append({"role": "user", "content": user_msg})
    st.chat_message("user").write(user_msg)

    contexto = build_knowledge_context()
    system_prompt = extract_system_prompt_from_docs()
    historico = "\n".join([f"{x['role']}: {x['content']}" for x in st.session_state.messages[-10:]])
    prompt = build_prompt(system_prompt, contexto, historico, user_msg)

    with st.spinner("Consultando agente de IA..."):
        resposta = ask_ollama(prompt, ollama_url, modelo, models, read_timeout=read_timeout)

    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.chat_message("assistant").write(resposta)
