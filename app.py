import streamlit as st
import carregar_dados_publicos as cd
import pandas as pd

def aplicar_tema(tema):

    if tema == "Escuro":
        fundo = "#0B1117"
        fundo_secundario = "#262730"
        texto = "#FAFAFA"
        texto_secundario = "#D1D5DB"
        borda = "#3A3A3A"
        input_fundo = "#262730"
        botao_fundo = "#1E293B"
        botao_texto = "#FAFAFA"

    else:
        fundo = "#FFFFFF"
        fundo_secundario = "#F3F5F7"
        texto = "#202124"
        texto_secundario = "#4B5563"
        borda = "#DADCE0"
        input_fundo = "#FFFFFF"
        botao_fundo = "#F3F5F7"
        botao_texto = "#202124"

    st.markdown(
        f"""
        <style>

        /* ========================================
           FUNDO PRINCIPAL
        ======================================== */

        .stApp {{
            background-color: {fundo} !important;
            color: {texto} !important;
        }}

        [data-testid="stHeader"] {{
            background-color: {fundo} !important;
        }}


        /* ========================================
           TEXTOS
        ======================================== */

        h1, h2, h3, h4, h5, h6, p, label {{
            color: {texto} !important;
        }}

        [data-testid="stMarkdownContainer"] p {{
            color: {texto} !important;
        }}


        /* ========================================
           INPUT DE TEXTO / SENHA
        ======================================== */

        [data-testid="stTextInput"] div[data-baseweb="input"] {{
            background-color: {input_fundo} !important;
            border-color: {borda} !important;
        }}

        [data-testid="stTextInput"] input {{
            background-color: {input_fundo} !important;
            color: {texto} !important;
            -webkit-text-fill-color: {texto} !important;
        }}

        /* Placeholder */
        [data-testid="stTextInput"] input::placeholder {{
            color: {texto_secundario} !important;
        }}

        /* Ícone do olho da senha */
        [data-testid="stTextInput"] svg {{
            color: {texto} !important;
            fill: {texto} !important;
        }}


        /* ========================================
           FORMULÁRIOS
        ======================================== */

        [data-testid="stForm"] {{
            background-color: {fundo} !important;
            border-color: {borda} !important;
        }}


        /* ========================================
           BOTÕES
        ======================================== */

        [data-testid="stFormSubmitButton"] button,
        [data-testid="stButton"] button {{
            background-color: {botao_fundo} !important;
            color: {botao_texto} !important;
            border: 1px solid {borda} !important;
        }}

        [data-testid="stFormSubmitButton"] button:hover,
        [data-testid="stButton"] button:hover {{
            border-color: #38BDF8 !important;
            color: #38BDF8 !important;
        }}

        [data-testid="stFormSubmitButton"] button p,
        [data-testid="stButton"] button p {{
            color: inherit !important;
        }}


        /* ========================================
           RADIO BUTTON
        ======================================== */

        [data-testid="stRadio"] label {{
            color: {texto} !important;
        }}

        [data-testid="stRadio"] p {{
            color: {texto} !important;
        }}


        /* ========================================
           MÉTRICAS
        ======================================== */

        [data-testid="stMetric"] {{
            background-color: {fundo_secundario} !important;
            border: 1px solid {borda} !important;
            padding: 15px;
            border-radius: 10px;
        }}

        [data-testid="stMetricValue"] {{
            color: {texto} !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: {texto} !important;
        }}


        /* ========================================
           ABAS
        ======================================== */

        .stTabs [data-baseweb="tab-list"] {{
            background-color: {fundo} !important;
        }}

        .stTabs [data-baseweb="tab"] p {{
            color: {texto_secundario} !important;
        }}

        .stTabs [aria-selected="true"] p {{
            color: #38BDF8 !important;
        }}

        .stTabs [data-baseweb="tab-highlight"] {{
            background-color: #38BDF8 !important;
        }}


        /* ========================================
           DIVISORES
        ======================================== */

        hr {{
            border-color: {borda} !important;
        }}


        /* ========================================
           DATAFRAMES / TABELAS
        ======================================== */

        [data-testid="stDataFrame"] {{
            background-color: {fundo_secundario} !important;
        }}


        /* ========================================
           SELECTBOX
        ======================================== */

        [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            background-color: {input_fundo} !important;
            color: {texto} !important;
            border-color: {borda} !important;
        }}


        </style>
        """,
        unsafe_allow_html=True
    )
st.set_page_config(
    page_title="Painel Saúde 2026",
    layout="wide",
    initial_sidebar_state="collapsed"
)

tema = st.radio(
    "Tema",
    ["Claro", "Escuro"],
    horizontal=True,
    index=1
)

aplicar_tema(tema)

#===================================================
#SENHA -> EU CONFIGURO ELA EM UM ARQUIVO SEPARADO
#===================================================

def solicitar_senha():
    
    
    if st.session_state.get("senha_correta", False):
        return True

    with st.form("tela_login"):
        st.warning("Acesso Restrito: Insira a senha para visualizar os dados.")
        senha_digitada = st.text_input("Senha", type="password")
        botao_entrar = st.form_submit_button("Entrar")

    if botao_entrar:
        if senha_digitada == st.secrets["senha_painel"]:
            st.session_state["senha_correta"] = True
            st.rerun() 
        else:
            st.error("Senha incorreta.")
    
    st.stop()


# Chama a trava de segurança logo no início
solicitar_senha()
#somente aopos confirmar pode ir
dados = cd.carregar_dados()

# Se houver algum erro a carregar o CSV, ele para por aqui de forma segura
if dados is None:
    st.stop()

st.title("Saúde 2026")
st.caption(
    "Dados atualizados até 08/10/2026. "
    "Os dados de outubro são parciais."
)
# Criando as abas

st.markdown(
    """
    <style>
    /* Muda a cor da linha brilhante embaixo da aba ativa */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #38BDF8 !important;
    }
    
    /* Muda a cor do texto da aba selecionada */
    .stTabs [aria-selected="true"] p {
        color: #38BDF8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
v_geral, aba_tconsulta, aba_medicos, consultas_distrito = st.tabs([
    "Visão Geral",
    "Atendimentos",
    "Consultas Médicas",
    "Por Distrito"
])


#===================================================
#DADOS GERAIS, VAI SER UMA TABELA SIMPLES
##===================================================
with v_geral:

    st.markdown(
    """
    <div style="
        background-color: #1E293B; 
        padding: 16px; 
        border-radius: 8px; 
        border-left: 4px solid #38BDF8;
        color: #38BDF8;
        font-family: sans-serif;
    ">
        Os indicadores apresentados referem-se aos dados disponíveis para 2026.
    </div>
    """,
    unsafe_allow_html=True
)

    st.subheader("Visão Geral")
    col1, col2, col3 = st.columns(3)


    with col1:
        st.metric(
            "Usuários atendidos",
            dados["total_usuarios_geral"]
        )

    with col2:
        st.metric(
            "Equipes",
            dados["total_equipes"]
        )

    with col3:
        st.metric(
            "Atendimentos médicos",
            dados["total_atend_medicos"]
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
    "Profissionais que ingressaram em 2026",
    dados["total_profissionais_2026"]
)
        



    with col5:
        st.metric(
            "Cadastros completos",
            "Em breve"
        )

    with col6:
        st.metric(
            "População IBGE",
            "Em breve"
        )

    st.divider()


#===================================================
#TOTAL DE CONSULTAS, ESTOU CONSIDERANDO MSM CNS, TIREI O TIPO = 5 PQ É ESCUTA INICIAL
##===================================================
with aba_tconsulta:
    col1, col2 = st.columns(2)
    with col1:
        # O primeiro texto é o que aparece no celular. O segundo é a variável exata do dicionário.
        st.metric("Usuários Atendidos", dados["total_usuarios_geral"])
    with col2:
        st.metric("Equipes Ativas", dados["total_equipes"])
    
    st.divider()
    st.markdown("**Total de Atendimentos por Mês**")
    
    # Renomear as colunas pra ficar mais facil de achar
    df_grafico = dados["atendimentos_mes"].rename(columns={
        "Mes_nome": "Mês",
        "total_atendimentos": "Total de Atendimentos"
    })
    
    # Grafico de barras
    st.bar_chart(
        df_grafico,
        x="Mês",
        y="Total de Atendimentos",
        height=500
    )

#===================================================
#TOTAL DE CONSULTAS DO CBO MEDICO
##===================================================
with aba_medicos:
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Consultas médicas",
            dados["total_atend_medicos"]
        )

    with col2:
        st.metric(
            "Pacientes únicos",
            dados["total_pessoas_medicas"]
        )

    st.divider()

    st.subheader("Consultas médicas por mês")

    st.bar_chart(
        dados["medicos_mes"],
        x="Mes_nome",
        y="total_consultas",
        height=500
    )

#===================================================
#TOTAL DE CONSULTAS DE PACIENTES SEPARADO POR DISTRITO
##===================================================
with consultas_distrito:

    st.subheader("Atendimentos por distrito")

    total_distritos = (
        dados["atendimentos_regiao"]["us_distrito"]
        .nunique()
    )

    st.metric(
        "Distritos com atendimentos",
        total_distritos
    )

    st.divider()

    df_grafico_regiao = dados["atendimentos_regiao"].rename(
        columns={
            "us_distrito": "Distrito",
            "total_atendimentos": "Atendimentos"
        }
    )

    st.bar_chart(
        df_grafico_regiao,
        x="Distrito",
        y="Atendimentos",
        height= 500
    )