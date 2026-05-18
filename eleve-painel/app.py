import streamlit as st
from datetime import date
from sheets import salvar_registro
from config import MINISTERIOS, CELEBRACAO_NOME

st.set_page_config(
    page_title="Painel Eleve · Igreja da Cidade",
    page_icon="✝️",
    layout="centered",
)

st.markdown(f"### ✝️ {CELEBRACAO_NOME}")
st.caption("Painel de registro · Igreja da Cidade")
st.divider()

nome = st.text_input("👤 Seu nome")
ministerio = st.selectbox("🏛️ Ministério", ["— Selecione —"] + MINISTERIOS)

if ministerio != "— Selecione —":
    st.divider()
    dados = {"nome": nome, "ministerio": ministerio, "quantidade": 0, "dec_primeira_vez": 0, "dec_jesus": 0, "dec_reconciliacao": 0, "dec_batismo": 0}

    if ministerio == "Primeira vez":
        dados["quantidade"] = st.number_input("👥 Voluntários", min_value=0, step=1)
        dados["dec_primeira_vez"] = st.number_input("🥇 Decisões — Primeira vez", min_value=0, step=1)

    elif ministerio == "Recomeço":
        dados["quantidade"] = st.number_input("👥 Voluntários", min_value=0, step=1)
        st.markdown("**Decisões:**")
        dados["dec_jesus"] = st.number_input("✝️ Jesus", min_value=0, step=1)
        dados["dec_reconciliacao"] = st.number_input("👐🏻 Reconciliação", min_value=0, step=1)
        dados["dec_batismo"] = st.number_input("🌊 Batismo", min_value=0, step=1)

    else:
        dados["quantidade"] = st.number_input("👥 Quantidade de pessoas", min_value=0, step=1)

    st.divider()

    if st.button("💾 Enviar", type="primary", use_container_width=True):
        if not nome.strip():
            st.warning("⚠️ Por favor, preencha seu nome antes de enviar.")
        else:
            data_hoje = date.today().strftime("%d/%m/%Y")
            with st.spinner("Enviando..."):
                try:
                    salvar_registro(dados, data_hoje, "")
                    st.success(f"✅ Registro de **{nome}** ({ministerio}) enviado com sucesso!")
                    if st.button("➕ Preencher outro ministério", use_container_width=True):st.reru()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar: {e}")