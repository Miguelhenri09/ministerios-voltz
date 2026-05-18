import streamlit as st
from datetime import date
from sheets import salvar_registro
from config import MINISTERIOS, CELEBRACAO_NOME

st.set_page_config(
    page_title="Painel Eleve · Igreja da Cidade",
    page_icon="✝️",
    layout="centered",
)

# --- TRATAMENTO DA CHAVE PRIVADA ---
if "gcp_service_account" in st.secrets:
    # Se você precisar recriar as quebras de linha para a biblioteca do Google:
    # Garante que o \n literal vire uma quebra de linha real de string do Python
    orig_key = st.secrets["gcp_service_account"]["private_key"]
    
    # Se a chave veio com \n escrito (literal), a gente troca por enter real
    if "\\n" in orig_key:
        st.secrets["gcp_service_account"]["private_key"] = orig_key.replace("\\n", "\n")
        
    # --- Fim do tratamento ---

# Inicializa session_state
if "enviado" not in st.session_state:
    st.session_state.enviado = False
if "ultimo_nome" not in st.session_state:
    st.session_state.ultimo_nome = ""
if "ultimo_ministerio" not in st.session_state:
    st.session_state.ultimo_ministerio = ""

st.markdown(f"### ✝️ {CELEBRACAO_NOME}")
st.caption("Painel de registro · Igreja da Cidade")
st.divider()

# Tela de sucesso
if st.session_state.enviado:
    st.success(f"✅ Registro de **{st.session_state.ultimo_nome}** ({st.session_state.ultimo_ministerio}) enviado com sucesso!")
    if st.button("➕ Preencher outro ministério", use_container_width=True):
        st.session_state.enviado = False
        st.rerun()
    st.stop()

# Formulário principal
nome = st.text_input("👤 Seu nome")

# Campo de data do culto
data_culto = st.date_input(
    "📅 Data do culto",
    value=date.today(),
    format="DD/MM/YYYY",
)

ministerio = st.selectbox("🏛️ Ministério", ["— Selecione —"] + MINISTERIOS)

if ministerio != "— Selecione —":
    st.divider()
    dados = {
        "nome": nome,
        "ministerio": ministerio,
        "quantidade": 0,
        "dec_primeira_vez": 0,
        "dec_jesus": 0,
        "dec_reconciliacao": 0,
        "dec_batismo": 0,
    }

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
            data_culto_str = data_culto.strftime("%d/%m/%Y")
            with st.spinner("Enviando..."):
                try:
                    salvar_registro(dados, data_culto_str)
                    st.session_state.ultimo_nome = nome
                    st.session_state.ultimo_ministerio = ministerio
                    st.session_state.enviado = True
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar: {type(e).__name__} - {str(e)}")
                    # Isso vai forçar o erro completo a aparecer no log do Streamlit Cloud também!
                raise e
