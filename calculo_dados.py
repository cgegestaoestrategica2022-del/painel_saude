import pandas as pd
import streamlit as st


@st.cache_data
def carregar_dados():

    try:

        colunas_esus = [
            "data_mes",
            "co_seq_fat_atd_ind",
            "cidadao_cns",
            "equipe_ine",
            "cbo_codigo",
            "co_dim_tipo_atendimento",
            "us_distrito"
        ]

        df = pd.read_csv(
            "e-sus.csv",
            usecols=colunas_esus,
            dtype={
                "co_seq_fat_atd_ind": "string",
                "cidadao_cns": "string",
                "equipe_ine": "string",
                "cbo_codigo": "string",
                "co_dim_tipo_atendimento": "string",
                "us_distrito": "string"
            }
        )


        cnes = pd.read_excel(
            "Dados Brutos.xlsx",
            header=2,
            usecols=[
                "Data de Entrada",
                "CNS do Profissional"
            ],
            dtype={
                "CNS do Profissional": "string"
            }
        )


    except FileNotFoundError:

        st.error("Uma das bases não foi encontrada.")

        return None


    

    # Ajuste dos meses
    if '-' in str(df['data_mes'].iloc[0]) or '/' in str(df['data_mes'].iloc[0]):
        df["mes_numero"] = pd.to_datetime(df["data_mes"], errors='coerce').dt.month
    else:
        df["mes_numero"] = pd.to_numeric(df["data_mes"], errors='coerce')

    meses = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }

    

    df["Mes_nome"] = df["mes_numero"].map(meses)
    df["Mes_nome"] = pd.Categorical(df["Mes_nome"], categories=meses.values(), ordered=True)

    atendimentos_mes = (
    df
    .groupby("Mes_nome", observed=True)["co_seq_fat_atd_ind"]
    .nunique()
    .reset_index(name="total_atendimentos")
)

    # Contagem geral usando APENAS o CNS
    total_usuarios_geral = df["cidadao_cns"].nunique()
    total_equipes = df["equipe_ine"].nunique()

    # Filtro para os médicos (ajustado para a nova coluna de códigos)
    df_medicos = df[
    (df["cbo_codigo"].astype(str).str.strip() == "225142")
    &
    (df["co_dim_tipo_atendimento"] != '5')
].copy()

    total_atendimentos_medicos = df_medicos["co_seq_fat_atd_ind"].nunique()

  
    total_pessoas_medicas = df_medicos["cidadao_cns"].nunique()

    medicos_mes = (
    df_medicos
    .groupby("Mes_nome", observed=True)["co_seq_fat_atd_ind"]
    .nunique()
    .reset_index(name="total_consultas")
)

    df["us_distrito"] = (
    df["us_distrito"]
    .fillna("NÃO INFORMADO")
)
    
    atendimentos_regiao = (
    df
    .groupby("us_distrito")["co_seq_fat_atd_ind"]
    .nunique()
    .reset_index(name="total_atendimentos")
    .sort_values("total_atendimentos", ascending=False)
)

  
# ==========================================
# CNES - PROFISSIONAIS QUE ENTRARAM EM 2026
# ==========================================

    cnes["Data de Entrada"] = pd.to_datetime(
        cnes["Data de Entrada"],
        dayfirst=True,
        errors="coerce"
    )

    cnes_2026 = cnes[
        (cnes["Data de Entrada"] >= pd.Timestamp("2026-01-01")) &
        (cnes["Data de Entrada"] < pd.Timestamp("2027-01-01"))
    ].copy()

    total_profissionais_2026 = (
        cnes_2026["CNS do Profissional"]
        .nunique()
    )

   

    return {
    "df_bruto": df,
    "atendimentos_mes": atendimentos_mes,
    "atendimentos_regiao": atendimentos_regiao,
    "medicos_mes": medicos_mes,
    "total_usuarios_geral": total_usuarios_geral,
    "total_equipes": total_equipes,
    "total_atend_medicos": total_atendimentos_medicos,
    "total_pessoas_medicas": total_pessoas_medicas,

    "cnes_2026": cnes_2026,
    "total_profissionais_2026": total_profissionais_2026
}