SPREADSHEET_ID = "1VkPsJIiXSu8fqRh26FnDvkKlWQPcCOlUkB1TNZ484Xg"
SHEET_NAME = "Sheet1"
CELEBRACAO_NOME = "CELEBRAÇÃO ELEVE VOLTZ"

SECOES = [
    {
        "nome": "FREQUÊNCIA",
        "campos": [
            {"chave": "freq_adolescentes", "label": "Adolescentes", "emoji": "👤"},
        ]
    },
    {
        "nome": "DECISÕES",
        "campos": [
            {"chave": "dec_jesus",         "label": "Jesus",         "emoji": "✝️"},
            {"chave": "dec_reconciliacao", "label": "Reconciliação",  "emoji": "👐🏻"},
            {"chave": "dec_batismo",       "label": "Batismo",        "emoji": "🌊"},
            {"chave": "dec_primeira_vez",  "label": "Primeira vez",   "emoji": "🥇"},
        ]
    },
    {
        "nome": "VOLUNTÁRIOS — Base de Adoração",
        "campos": [
            {"chave": "vol_louvor",       "label": "Louvor",               "emoji": "🎸"},
            {"chave": "vol_som",          "label": "Técnica Som",           "emoji": "🎛️"},
            {"chave": "vol_iluminacao",   "label": "Técnica Iluminação",    "emoji": "💡"},
            {"chave": "vol_multimidia",   "label": "Multimídia",            "emoji": "🎥"},
            {"chave": "vol_comunicacoes", "label": "Comunicações",          "emoji": "🗣️"},
            {"chave": "vol_ordem_culto",  "label": "Ordem de culto",        "emoji": "📄"},
            {"chave": "vol_intercessao",  "label": "Intercessão",           "emoji": "🤲🏻"},
            {"chave": "vol_posso_orar",   "label": "Posso Orar",            "emoji": "🙏🏻"},
            {"chave": "vol_danca",        "label": "Dança",                 "emoji": "🩰"},
        ]
    },
    {
        "nome": "VOLUNTÁRIOS — Base de Comunhão",
        "campos": [
            {"chave": "com_recomeco",     "label": "Recomeço",     "emoji": "↪️"},
            {"chave": "com_primeira_vez", "label": "Primeira vez", "emoji": "🥇"},
            {"chave": "com_central",      "label": "Central",      "emoji": "🔗"},
        ]
    },
    {
        "nome": "VOLUNTÁRIOS — Base de Serviço",
        "campos": [
            {"chave": "serv_atm",       "label": "ATM",                 "emoji": "🤝"},
            {"chave": "serv_brigada",   "label": "Brigada de Incêndio", "emoji": "👩‍🚒"},
            {"chave": "serv_ignicao",   "label": "Ignição",             "emoji": "🧸"},
            {"chave": "serv_estacion",  "label": "Estacionamento",      "emoji": "🚗"},
        ]
    },
]

CABECALHOS = ["data_registro", "data_culto", "dia_semana"] + [
    chave
    for secao in SECOES
    for campo in secao["campos"]
    for chave in [campo["chave"] + "_qtd", campo["chave"] + "_nomes"]
]