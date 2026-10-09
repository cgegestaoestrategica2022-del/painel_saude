from pathlib import Path
import pandas as pd
import calculo_dados as cd


# ==========================================
# CARREGA OS DADOS CALCULADOS
# ==========================================

dados = cd.carregar_dados()

if dados is None:
    raise RuntimeError("Não foi possível carregar as bases.")


# ==========================================
# CRIA A PASTA DE DADOS PÚBLICOS
# ==========================================

pasta = Path("dados_publicos")

pasta.mkdir(
    exist_ok=True
)


# ==========================================
# INDICADORES GERAIS
# ==========================================

indicadores_gerais = pd.DataFrame({
    "indicador": [
        "usuarios_atendidos",
        "equipes",
        "consultas_medicas",
        "pacientes_medicos_unicos",
        "profissionais_ingressantes_2026"
    ],

    "valor": [
        dados["total_usuarios_geral"],
        dados["total_equipes"],
        dados["total_atend_medicos"],
        dados["total_pessoas_medicas"],
        dados["total_profissionais_2026"]
    ]
})


indicadores_gerais.to_csv(
    pasta / "indicadores_gerais.csv",
    index=False
)


# ==========================================
# ATENDIMENTOS POR MÊS
# ==========================================

dados["atendimentos_mes"].to_csv(
    pasta / "atendimentos_mes.csv",
    index=False
)


# ==========================================
# CONSULTAS MÉDICAS POR MÊS
# ==========================================

dados["medicos_mes"].to_csv(
    pasta / "medicos_mes.csv",
    index=False
)


# ==========================================
# ATENDIMENTOS POR DISTRITO
# ==========================================

dados["atendimentos_regiao"].to_csv(
    pasta / "atendimentos_distrito.csv",
    index=False
)


print("Dados públicos gerados com sucesso!")