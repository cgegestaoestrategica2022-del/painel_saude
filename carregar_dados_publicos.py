from pathlib import Path

import pandas as pd
import streamlit as st


@st.cache_data
def carregar_dados():

    raiz = Path(__file__).parent
    pasta = raiz / "dados_publicos"

    # ==============================
    # INDICADORES GERAIS
    # ==============================

    indicadores_df = pd.read_csv(
        pasta / "indicadores_gerais.csv"
    )

    indicadores = dict(
        zip(
            indicadores_df["indicador"],
            indicadores_df["valor"]
        )
    )

    # ==============================
    # GRÁFICOS
    # ==============================

    atendimentos_mes = pd.read_csv(
        pasta / "atendimentos_mes.csv"
    )

    medicos_mes = pd.read_csv(
        pasta / "medicos_mes.csv"
    )

    atendimentos_regiao = pd.read_csv(
        pasta / "atendimentos_distrito.csv"
    )

    # ==============================
    # RETORNO
    # ==============================

    return {
        "atendimentos_mes": atendimentos_mes,
        "atendimentos_regiao": atendimentos_regiao,
        "medicos_mes": medicos_mes,

        "total_usuarios_geral":
            indicadores["usuarios_atendidos"],

        "total_equipes":
            indicadores["equipes"],

        "total_atend_medicos":
            indicadores["consultas_medicas"],

        "total_pessoas_medicas":
            indicadores["pacientes_medicos_unicos"],

        "total_profissionais_2026":
            indicadores["profissionais_ingressantes_2026"]
    }