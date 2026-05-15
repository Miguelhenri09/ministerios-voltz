import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import streamlit as st
from config import SPREADSHEET_ID, SHEET_NAME, CABECALHOS

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def conectar_planilha():
    if "gcp_service_account" in st.secrets:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=SCOPES)
    else:
        from dotenv import load_dotenv
        load_dotenv()
        credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials/service_account.json")
        creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)

    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

def garantir_cabecalhos(aba):
    if not aba.row_values(1):
        aba.append_row(CABECALHOS)

def salvar_registro(dados: dict, data_culto: str, dia_semana: str):
    aba = conectar_planilha()
    garantir_cabecalhos(aba)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = [
        agora,
        dados.get("nome", ""),
        dados.get("ministerio", ""),
        dados.get("quantidade", 0),
        dados.get("dec_primeira_vez", 0),
        dados.get("dec_jesus", 0),
        dados.get("dec_reconciliacao", 0),
        dados.get("dec_batismo", 0),
    ]
    aba.append_row(linha, value_input_option="USER_ENTERED")