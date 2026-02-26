from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from jornada_core import (
    compute_scenarios,
    detect_out_of_scope,
    empathetic_wrap,
    estimate_goal_by_keywords,
    feasible_feedback,
    format_currency,
    load_json,
    parse_currency,
    parse_months,
    save_json,
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
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


def append_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})


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
