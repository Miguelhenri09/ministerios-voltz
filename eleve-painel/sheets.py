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
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
    else:
        from dotenv import load_dotenv
        load_dotenv()
        credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials/service_account.json")
        creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)

    client = gspread.authorize(creds)
    planilha = client.open_by_key(SPREADSHEET_ID)
    aba = planilha.worksheet(SHEET_NAME)
    return aba


def garantir_cabecalhos(aba):
    primeira_linha = aba.row_values(1)
    if not primeira_linha:
        aba.append_row(CABECALHOS)


def salvar_registro(dados: dict, data_culto: str, dia_semana: str) -> bool:
    try:
        aba = conectar_planilha()
        garantir_cabecalhos(aba)

        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        linha = [agora, data_culto, dia_semana]

        for cabecalho in CABECALHOS[3:]:
            linha.append(dados.get(cabecalho, ""))

        aba.append_row(linha, value_input_option="USER_ENTERED")
        return True

    except Exception as e:
        print(f"Erro ao salvar no Sheets: {e}")
        raise e