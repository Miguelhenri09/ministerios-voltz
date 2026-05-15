import streamlit as st
from datetime import date
from sheets import salvar_registro
from config import SECOES, CELEBRACAO_NOME

st.set_page_config(
    page_title="Painel Eleve · Igreja da Cidade",
    page_icon="✝️",
    layout="centered",
)

st.markdown("""
<style>
    .titulo-painel { font-size: 1.6rem; font-weight: 700; color: #1a1a2e; }
    .subtitulo-painel { font-size: 0.95rem; color: #666; margin-bottom: 1.5rem; }
    .secao-titulo { font-size: 1rem; font-weight: 700; color: #333; background: #f0f2f6; padding: 6px 12px; border-radius: 6px; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="titulo-painel">✝️ {CELEBRACAO_NOME}</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo-painel">Painel de registro · Igreja da Cidade</div>', unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    data_culto = st.date_input("📅 Data do culto", value=date.today())
with col2:
    DIAS_PT = {"Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira", "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"}
    dia_semana = DIAS_PT[data_culto.strftime("%A")]
    st.markdown(f"<br><b>{dia_semana}</b>", unsafe_allow_html=True)

st.divider()
dados = {}

for secao in SECOES:
    st.markdown(f'<div class="secao-titulo">📋 {secao["nome"]}</div>', unsafe_allow_html=True)
    for campo in secao["campos"]:
        chave = campo["chave"]
        col_qtd, col_nomes = st.columns([1, 3])
        with col_qtd:
            qtd = st.number_input(f'{campo["emoji"]} {campo["label"]} — Qtd', min_value=0, step=1, key=f"{chave}_qtd")
        with col_nomes:
            nomes = st.text_input(f'Nomes ({campo["label"]})', placeholder="Ex: Ana, João, Maria...", key=f"{chave}_nomes")
        dados[f"{chave}_qtd"] = qtd
        dados[f"{chave}_nomes"] = nomes

st.divider()

if st.button("💾 Salvar relatório no Google Sheets", type="primary", use_container_width=True):
    data_formatada = data_culto.strftime("%d/%m/%Y")
    with st.spinner("Enviando para o Google Sheets..."):
        try:
            salvar_registro(dados, data_formatada, dia_semana)
            st.success("✅ Relatório salvo com sucesso na planilha!")
            st.markdown("---")
            st.markdown("**📋 Mensagem formatada para WhatsApp:**")
            linhas = [CELEBRACAO_NOME, f"{data_formatada} - {dia_semana}", ""]
            for secao in SECOES:
                linhas.append(secao["nome"].replace("VOLUNTÁRIOS — ", ""))
                for campo in secao["campos"]:
                    chave = campo["chave"]
                    qtd = dados.get(f"{chave}_qtd", 0)
                    nomes = dados.get(f"{chave}_nomes", "")
                    linha = f'{campo["emoji"]} {campo["label"]}: {qtd}'
                    if nomes:
                        linha += f" ({nomes})"
                    linhas.append(linha)
                linhas.append("")
            st.code("\n".join(linhas).strip(), language=None)
        except Exception as e:
            st.error(f"❌ Erro ao salvar: {e}")