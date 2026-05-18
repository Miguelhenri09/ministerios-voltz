import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json
import streamlit as st
from config import SPREADSHEET_ID, SHEET_NAME, CABECALHOS

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def conectar_planilha():
    if "gcp_service_account" in st.secrets:
        info = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"].replace("\\n", "\n"),
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
        }
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    else:
        credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials/service_account.json")
        creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)

    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
                                                        
def garantir_cabecalhos(aba):
    if not aba.row_values(1):
        aba.append_row(CABECALHOS)

def salvar_registro(dados: dict, data_culto: str):
    aba = conectar_planilha()
    garantir_cabecalhos(aba)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = [
        agora,
        data_culto,
        dados.get("nome", ""),
        dados.get("ministerio", ""),
        dados.get("quantidade", 0),
        dados.get("dec_primeira_vez", 0),
        dados.get("dec_jesus", 0),
        dados.get("dec_reconciliacao", 0),
        dados.get("dec_batismo", 0),
    ]
    aba.append_row(linha, value_input_option="USER_ENTERED")