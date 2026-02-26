from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from jornada_core import (
<<<<<<< HEAD
    build_goals_context,
    build_knowledge_context,
    compute_scenarios,
    configure_ollama,
    detect_goal_detail_intent,
    detect_help_intent,
    detect_list_goals_intent,
    detect_new_goal_intent,
    detect_out_of_scope,
    detect_restart_intent,
    estimate_goal_by_keywords,
    extract_system_prompt,
    feasible_feedback,
    format_currency,
    generate_agent_reply,
    load_json,
    ollama_health,
    parse_currency,
    parse_months,
    prettify_dream_name,
=======
    compute_scenarios,
    detect_out_of_scope,
    empathetic_wrap,
    estimate_goal_by_keywords,
    feasible_feedback,
    format_currency,
    load_json,
    parse_currency,
    parse_months,
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
    save_json,
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
<<<<<<< HEAD
DOCS_DIR = BASE_DIR / "docs"
CONTEXT_FILE = DATA_DIR / "jornada_contexto.json"
PROMPTS_FILE = DOCS_DIR / "03-prompts.md"
KNOWLEDGE_FILE = DOCS_DIR / "02-base-conhecimento.md"

SAFETY_NOTICE = (
    "Agente educativo de metas financeiras. Nao recomenda ativos especificos "
    "e nao substitui orientacao profissional."
)

VALID_STAGES = {"idle", "collect_name", "collect_target", "collect_term", "collect_initial", "collect_income"}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def default_user_state(user_id: str):
    return {
        "id_usuario": user_id,
        "etapa": "idle",
        "metas": [],
        "rascunho_meta": None,
        "updated_at": None,
    }


def migrate_user_state(state: dict, user_id: str):
    data = dict(state) if isinstance(state, dict) else {}
    data.setdefault("id_usuario", user_id)
    data.setdefault("metas", [])
    data.setdefault("rascunho_meta", None)
    if data.get("etapa") not in VALID_STAGES:
        data["etapa"] = "idle"

    # migra formato antigo de meta unica
    if not data["metas"] and data.get("nome_sonho") and data.get("valor_meta") and data.get("prazo_meses"):
        cenarios = compute_scenarios(
            float(data["valor_meta"]),
            float(data.get("valor_inicial", 0.0)),
            int(data["prazo_meses"]),
        )
        data["metas"].append(
            {
                "id_meta": 1,
                "nome_sonho": str(data["nome_sonho"]),
                "valor_meta": float(data["valor_meta"]),
                "prazo_meses": int(data["prazo_meses"]),
                "valor_inicial": float(data.get("valor_inicial", 0.0)),
                "renda_mensal": float(data.get("renda_mensal", 0.0)),
                "cenarios": cenarios,
                "status": "ativa",
                "created_at": data.get("updated_at") or now_iso(),
                "updated_at": now_iso(),
            }
        )
    return data


def persist_state(all_states: dict, user_id: str, user_state: dict):
    user_state["updated_at"] = now_iso()
    all_states[user_id] = user_state
    save_json(CONTEXT_FILE, all_states)
=======
CONTEXT_FILE = DATA_DIR / "jornada_contexto.json"
PERFIL_FILE = DATA_DIR / "perfil_investidor.json"

SAFETY_NOTICE = (
    "Este simulador é educativo e usa cenários hipotéticos de rendimento. "
    "Não é recomendação de investimento e não substitui orientação profissional."
)


def get_profile_income():
    profile = load_json(PERFIL_FILE, {})
    income = profile.get("renda_mensal")
    return float(income) if isinstance(income, (int, float)) else 0.0


def initial_bot_message(context):
    if context.get("nome_sonho"):
        return (
            f"Olá! Como estamos na missão para {context['nome_sonho']}? "
            "Se quiser, recalculo seu plano com novos valores."
        )
    return (
        "Oi, eu sou a Jornada. Vou te ajudar a transformar um sonho em um plano matemático. "
        "Qual sonho você quer viver?"
    )


st.set_page_config(page_title="Jornada dos Sonhos", page_icon="🎯", layout="centered")
st.title("🎯 Jornada dos Sonhos")
st.caption(SAFETY_NOTICE)

all_contexts = load_json(CONTEXT_FILE, {})
default_income = get_profile_income()

if "user_id" not in st.session_state:
    st.session_state.user_id = "user_001"

user_id = st.sidebar.text_input("ID do usuário", value=st.session_state.user_id).strip() or "user_001"
st.session_state.user_id = user_id

current = all_contexts.get(
    user_id,
    {
        "id_usuario": user_id,
        "nome_sonho": "",
        "valor_meta": None,
        "prazo_meses": None,
        "valor_inicial": 0.0,
        "perfil_risco": "iniciante",
        "renda_mensal": default_income,
        "etapa": "descoberta",
        "updated_at": None,
    },
)

if "messages" not in st.session_state or st.session_state.get("messages_user") != user_id:
    st.session_state.messages = [{"role": "assistant", "content": initial_bot_message(current)}]
    st.session_state.messages_user = user_id

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0


def append_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})


<<<<<<< HEAD
def next_goal_id(user_state: dict):
    metas = user_state.get("metas", [])
    if not metas:
        return 1
    return max(int(item.get("id_meta", 0)) for item in metas) + 1


def reset_goal_creation(user_state: dict):
    user_state["etapa"] = "idle"
    user_state["rascunho_meta"] = None


def list_goals_text(user_state: dict):
    metas = user_state.get("metas", [])
    if not metas:
        return "Voce ainda nao tem metas cadastradas. Diga: `nova meta`."
    lines = ["Metas cadastradas:"]
    for item in metas:
        lines.append(
            f"{item['id_meta']}. {item['nome_sonho']} | "
            f"Meta: {format_currency(item['valor_meta'])} | "
            f"Prazo: {item['prazo_meses']} meses | Status: {item['status']}"
        )
    lines.append("Para detalhes: `meta 1`.")
    return "\n".join(lines)


def goal_detail_text(user_state: dict, goal_id: int):
    goal = next((x for x in user_state.get("metas", []) if int(x.get("id_meta", 0)) == goal_id), None)
    if not goal:
        return f"Nao encontrei a meta {goal_id}. Use `listar metas`."
    cenarios = goal.get("cenarios") or compute_scenarios(goal["valor_meta"], goal["valor_inicial"], goal["prazo_meses"])
    return (
        f"Meta {goal['id_meta']} - {goal['nome_sonho']}\n"
        f"- Valor-meta: {format_currency(goal['valor_meta'])}\n"
        f"- Prazo: {goal['prazo_meses']} meses\n"
        f"- Valor inicial: {format_currency(goal['valor_inicial'])}\n"
        f"- Aporte conservador: {format_currency(cenarios['conservador']['aporte'])}/mes\n"
        f"- Aporte moderado: {format_currency(cenarios['moderado']['aporte'])}/mes"
    )


def start_new_goal_flow(user_state: dict, raw_dream: str | None = None):
    user_state["rascunho_meta"] = {
        "nome_sonho": "",
        "valor_meta": None,
        "prazo_meses": None,
        "valor_inicial": 0.0,
        "renda_mensal": 0.0,
    }
    if raw_dream:
        dream_name = prettify_dream_name(raw_dream)
        faixa, obs = estimate_goal_by_keywords(dream_name)
        user_state["rascunho_meta"]["nome_sonho"] = dream_name
        user_state["etapa"] = "collect_target"
        return (
            f"Perfeito. Seu sonho ficou como **{dream_name}**.\n"
            f"Faixa de referencia: {format_currency(faixa[0])} a {format_currency(faixa[1])} ({obs}).\n"
            "Qual valor-meta voce quer usar?"
        )
    user_state["etapa"] = "collect_name"
    return "Vamos criar uma nova meta. Qual sonho voce quer organizar?"


def complete_goal(user_state: dict):
    draft = user_state["rascunho_meta"]
    cenarios = compute_scenarios(draft["valor_meta"], draft["valor_inicial"], draft["prazo_meses"])
    warning = feasible_feedback(
        cenarios["moderado"]["aporte"],
        draft.get("renda_mensal", 0.0),
        draft["valor_meta"],
        draft["valor_inicial"],
    )
    goal = {
        "id_meta": next_goal_id(user_state),
        "nome_sonho": draft["nome_sonho"],
        "valor_meta": draft["valor_meta"],
        "prazo_meses": draft["prazo_meses"],
        "valor_inicial": draft["valor_inicial"],
        "renda_mensal": draft.get("renda_mensal", 0.0),
        "cenarios": cenarios,
        "status": "ativa",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    user_state["metas"].append(goal)
    reset_goal_creation(user_state)

    msg = (
        f"Meta salva com sucesso: {goal['nome_sonho']} (ID {goal['id_meta']})\n"
        f"- Meta: {format_currency(goal['valor_meta'])}\n"
        f"- Prazo: {goal['prazo_meses']} meses\n"
        f"- Valor inicial: {format_currency(goal['valor_inicial'])}\n"
        f"- Conservador: {format_currency(cenarios['conservador']['aporte'])}/mes\n"
        f"- Moderado: {format_currency(cenarios['moderado']['aporte'])}/mes"
    )
    if warning:
        msg += f"\n{warning}"
    msg += "\nSe quiser, diga `nova meta` ou `listar metas`."
    return msg


def handle_goal_collection(user_message: str, user_state: dict):
    etapa = user_state.get("etapa", "idle")
    draft = user_state.get("rascunho_meta") or {}

    if etapa == "collect_name":
        draft["nome_sonho"] = prettify_dream_name(user_message)
        faixa, obs = estimate_goal_by_keywords(draft["nome_sonho"])
        user_state["rascunho_meta"] = draft
        user_state["etapa"] = "collect_target"
        return (
            f"Legal, ficou: **{draft['nome_sonho']}**.\n"
            f"Faixa de referencia: {format_currency(faixa[0])} a {format_currency(faixa[1])} ({obs}).\n"
            "Qual valor-meta?"
        )

    if etapa == "collect_target":
        value = parse_currency(user_message)
        if value is None or value < 1000:
            return "Nao entendi o valor-meta. Exemplo: `35000` ou `R$ 35.000`."
        draft["valor_meta"] = round(value, 2)
        user_state["rascunho_meta"] = draft
        user_state["etapa"] = "collect_term"
        return "Em quanto tempo voce quer realizar (meses ou anos)?"

    if etapa == "collect_term":
        months = parse_months(user_message)
        if months is None or months <= 0:
            return "Nao entendi o prazo. Exemplo: `24 meses` ou `2 anos`."
        if months > 720:
            return "Prazo muito alto. Use ate 720 meses."
        draft["prazo_meses"] = months
        user_state["rascunho_meta"] = draft
        user_state["etapa"] = "collect_initial"
        return "Quanto voce ja tem guardado para essa meta? (pode ser 0)"

    if etapa == "collect_initial":
        initial = parse_currency(user_message)
        if initial is None:
            return "Nao entendi o valor inicial. Exemplo: `5000` ou `0`."
        draft["valor_inicial"] = round(initial, 2)
        user_state["rascunho_meta"] = draft
        user_state["etapa"] = "collect_income"
        return "Para checar viabilidade, qual sua renda mensal? (ou `0` se nao quiser informar)"

    if etapa == "collect_income":
        income = parse_currency(user_message)
        if income is None:
            return "Nao entendi a renda. Exemplo: `7200`."
        draft["renda_mensal"] = round(income, 2)
        user_state["rascunho_meta"] = draft
        return complete_goal(user_state)

    return "Nao ha cadastro em andamento. Diga `nova meta`."


def should_start_goal_flow(message: str):
    text = message.lower()
    return detect_new_goal_intent(message) and not detect_help_intent(message) and "como funciona" not in text


st.set_page_config(page_title="Jornada dos Sonhos", page_icon="🎯", layout="centered")
st.title("🎯 Jornada - Agente de IA")
st.caption(SAFETY_NOTICE)

st.sidebar.header("Ollama")
ollama_url = st.sidebar.text_input("URL API", value="http://localhost:11434/api/generate")
ollama_model = st.sidebar.text_input("Modelo", value="gpt-oss")
use_ollama = st.sidebar.checkbox("Usar Ollama", value=True)
configure_ollama(url=ollama_url, model=ollama_model)
ollama_online, models_online = ollama_health()
if ollama_online:
    st.sidebar.success("Ollama conectado")
    if models_online:
        st.sidebar.caption("Modelos: " + ", ".join(models_online))
else:
    st.sidebar.warning("Ollama offline (fallback textual local)")

all_states = load_json(CONTEXT_FILE, {})
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_001"
user_id = st.sidebar.text_input("ID usuario", value=st.session_state.user_id).strip() or "user_001"
st.session_state.user_id = user_id

current_state = migrate_user_state(all_states.get(user_id, default_user_state(user_id)), user_id)

if "messages" not in st.session_state or st.session_state.get("messages_user") != user_id:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Oi, eu sou a Jornada. Sou um agente de IA para planejamento financeiro por metas. "
                "Posso explicar como funciona, criar metas, listar metas e detalhar simulacoes."
            ),
        }
    ]
    st.session_state.messages_user = user_id

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_message = st.chat_input("Converse com a Jornada")

if user_message:
    append_message("user", user_message)
    st.chat_message("user").write(user_message)
    reply = None

    # guardrail de escopo
    out_scope = detect_out_of_scope(user_message)
    if out_scope:
        reply = out_scope

    # reinicio de fluxo de criacao
    if reply is None and detect_restart_intent(user_message):
        reset_goal_creation(current_state)
        reply = "Fluxo atual reiniciado. Se quiser criar outra meta, diga `nova meta`."

    # CRUD de metas
    if reply is None and detect_list_goals_intent(user_message):
        reply = list_goals_text(current_state)

    if reply is None:
        detail_id = detect_goal_detail_intent(user_message)
        if detail_id is not None:
            reply = goal_detail_text(current_state, detail_id)

    # fluxo em andamento
    if reply is None and current_state.get("etapa") != "idle":
        reply = handle_goal_collection(user_message, current_state)

    # iniciar nova meta
    if reply is None and should_start_goal_flow(user_message):
        reply = start_new_goal_flow(current_state, raw_dream=user_message)

    # resposta de agente IA baseada em docs + base
    if reply is None:
        prompts_md = PROMPTS_FILE.read_text(encoding="utf-8") if PROMPTS_FILE.exists() else ""
        system_prompt = extract_system_prompt(prompts_md)
        docs_context = KNOWLEDGE_FILE.read_text(encoding="utf-8") if KNOWLEDGE_FILE.exists() else ""
        knowledge_context = build_knowledge_context(DATA_DIR)
        goals_context = build_goals_context(current_state.get("metas", []))

        if use_ollama and ollama_online:
            llm_reply = generate_agent_reply(
                user_message=user_message,
                system_prompt=system_prompt,
                docs_context=docs_context,
                knowledge_context=knowledge_context,
                goals_context=goals_context,
                messages=st.session_state.messages,
            )
            reply = llm_reply or (
                "Nao consegui gerar resposta agora. Tente novamente ou use `nova meta`, `listar metas`."
            )
        else:
            if detect_help_intent(user_message):
                reply = (
                    "Funciona em 3 passos: criar meta, simular aporte e acompanhar progresso. "
                    "Comandos uteis: `nova meta`, `listar metas`, `meta 1`."
                )
            else:
                reply = (
                    "Posso te ajudar com planejamento financeiro por metas. "
                    "Diga seu sonho ou use `nova meta`."
                )

    append_message("assistant", reply)
    st.chat_message("assistant").write(reply)
    persist_state(all_states, user_id, current_state)

if current_state.get("metas"):
    st.divider()
    st.subheader("Metas do usuario")
    table = []
    for goal in current_state["metas"]:
        table.append(
            {
                "ID": goal["id_meta"],
                "Meta": goal["nome_sonho"],
                "Valor Meta": format_currency(goal["valor_meta"]),
                "Prazo (meses)": goal["prazo_meses"],
                "Status": goal["status"],
            }
        )
    st.dataframe(table, use_container_width=True, hide_index=True)
=======
def persist_current(context_obj):
    context_obj["updated_at"] = datetime.now(timezone.utc).isoformat()
    all_contexts[user_id] = context_obj
    save_json(CONTEXT_FILE, all_contexts)


user_input = st.chat_input("Conte seu sonho ou envie um dado da simulação")

if user_input:
    append_message("user", user_input)
    st.chat_message("user").write(user_input)

    etapa = current.get("etapa", "descoberta")
    reply = detect_out_of_scope(user_input) or ""

    if reply:
        append_message("assistant", reply)
        st.chat_message("assistant").write(reply)
        persist_current(current)
        st.stop()

    if etapa == "descoberta":
        current["nome_sonho"] = user_input.strip()
        faixa, obs = estimate_goal_by_keywords(current["nome_sonho"])
        current["faixa_estimativa"] = faixa
        current["etapa"] = "valor_meta"
        core = (
            f"Amei seu objetivo: {current['nome_sonho']}. "
            f"Uma estimativa inicial fica entre {format_currency(faixa[0])} e {format_currency(faixa[1])} "
            f"({obs}). Qual valor vamos definir como linha de chegada?"
        )
        reply = empathetic_wrap(
            core,
            current["nome_sonho"],
            user_context=f"- renda_mensal: {format_currency(current.get('renda_mensal', 0.0))}",
        )

    elif etapa == "valor_meta":
        value = parse_currency(user_input)
        if value is None or value < 1000:
            reply = "Não consegui entender o valor da meta. Me diga um valor como `35000` ou `R$ 35.000`."
        else:
            current["valor_meta"] = round(value, 2)
            current["etapa"] = "prazo"
            reply = "Perfeito. Em quanto tempo você quer realizar esse sonho? Pode ser em meses ou anos."

    elif etapa == "prazo":
        months = parse_months(user_input)
        if months is None or months <= 0:
            reply = "Não consegui entender o prazo. Exemplo: `24 meses` ou `2 anos`."
        elif months > 720:
            reply = "Esse prazo está longo demais para a simulação. Use até 720 meses."
        else:
            current["prazo_meses"] = months
            current["etapa"] = "valor_inicial"
            reply = "Você já tem algum valor guardado para essa meta? Se não tiver, pode responder `0`."

    elif etapa == "valor_inicial":
        initial_value = parse_currency(user_input)
        if initial_value is None:
            reply = "Não consegui entender o valor inicial. Responda com um número, ex.: `5000` ou `0`."
        else:
            current["valor_inicial"] = round(initial_value, 2)
            current["etapa"] = "renda"
            if current.get("renda_mensal", 0) > 0:
                reply = (
                    f"Uso sua renda mensal cadastrada de {format_currency(current['renda_mensal'])}. "
                    "Se quiser atualizar, envie o novo valor; se preferir manter, escreva `ok`."
                )
            else:
                reply = "Para checar viabilidade, me diga sua renda mensal aproximada."

    elif etapa == "renda":
        if user_input.strip().lower() != "ok":
            income = parse_currency(user_input)
            if income is None or income <= 0:
                reply = "Digite sua renda mensal em número (ex.: `5000`) ou `ok` para usar o valor atual."
                append_message("assistant", reply)
                st.chat_message("assistant").write(reply)
                persist_current(current)
                st.stop()
            current["renda_mensal"] = round(income, 2)

        current["etapa"] = "concluido"
        cenarios = compute_scenarios(current["valor_meta"], current["valor_inicial"], current["prazo_meses"])
        cons = cenarios["conservador"]["aporte"]
        mod = cenarios["moderado"]["aporte"]

        core = (
            f"Plano para {current['nome_sonho']}:\n"
            f"- Meta: {format_currency(current['valor_meta'])}\n"
            f"- Prazo: {current['prazo_meses']} meses\n"
            f"- Valor inicial: {format_currency(current['valor_inicial'])}\n"
            f"- Cenário conservador (0,5% a.m.): aporte de {format_currency(cons)} por mês\n"
            f"- Cenário moderado (0,8% a.m.): aporte de {format_currency(mod)} por mês\n"
        )

        warning = feasible_feedback(
            mod, current.get("renda_mensal", 0.0), current["valor_meta"], current["valor_inicial"]
        )
        if warning:
            core = f"{core}\n{warning}"

        reply = empathetic_wrap(
            core,
            current["nome_sonho"],
            user_context=(
                f"- valor_meta: {format_currency(current['valor_meta'])}\n"
                f"- prazo_meses: {current['prazo_meses']}\n"
                f"- valor_inicial: {format_currency(current['valor_inicial'])}\n"
                f"- renda_mensal: {format_currency(current.get('renda_mensal', 0.0))}"
            ),
        )

    else:
        reply = (
            "Podemos recalcular agora. Envie `reiniciar` para montar um novo plano, "
            "ou envie novo valor/prazo para ajustar."
        )
        lower = user_input.strip().lower()
        if lower == "reiniciar":
            current["etapa"] = "descoberta"
            current["nome_sonho"] = ""
            current["valor_meta"] = None
            current["prazo_meses"] = None
            current["valor_inicial"] = 0.0
            reply = "Combinado. Qual sonho você quer viver agora?"

    append_message("assistant", reply)
    st.chat_message("assistant").write(reply)
    persist_current(current)

if current.get("etapa") == "concluido" and current.get("valor_meta") and current.get("prazo_meses"):
    st.divider()
    st.subheader("Resumo da jornada")
    st.write(f"Sonho: **{current['nome_sonho']}**")
    st.write(f"Meta: **{format_currency(current['valor_meta'])}**")
    st.write(f"Prazo: **{current['prazo_meses']} meses**")
    st.write(f"Valor inicial: **{format_currency(current['valor_inicial'])}**")
    st.caption("Você pode continuar no chat para recalibrar prazos e valores.")
>>>>>>> 37ed0d9abeb5cea0474d5dfcf63ae59aa0e755e0
