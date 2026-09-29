import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Flamengo Stats")

jogos = pd.read_csv("jogos.csv")


def resultado(linha):
    if linha["gols_flamengo"] > linha["gols_adversario"]:
        return "V"
    elif linha["gols_flamengo"] == linha["gols_adversario"]:
        return "E"
    else:
        return "D"


jogos["resultado"] = jogos.apply(resultado, axis=1)
jogos["pontos"] = jogos["resultado"].map({"V": 3, "E": 1, "D": 0})
jogos["saldo"] = jogos["gols_flamengo"] - jogos["gols_adversario"]

st.sidebar.header("Filtros")
opcao_local = st.sidebar.radio("Local dos jogos", ["Todos", "Casa", "Fora"])

if opcao_local == "Todos":
    filtrados = jogos
else:
    filtrados = jogos[jogos["local"] == opcao_local.lower()]

total_jogos = len(filtrados)
total_pontos = filtrados["pontos"].sum()
aproveitamento = total_pontos / (total_jogos * 3) * 100
saldo_total = filtrados["saldo"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Jogos", total_jogos)
col2.metric("Pontos", total_pontos)
col3.metric("Aproveitamento", f"{aproveitamento:.1f}%")
col4.metric("Saldo de gols", saldo_total)

por_local = jogos.groupby("local").agg(
    partidas=("pontos", "count"),
    pontos=("pontos", "sum"),
    saldo=("saldo", "sum"),
)
por_local["aproveitamento"] = (por_local["pontos"] / (por_local["partidas"] * 3) * 100).round(1)

grafico = px.bar(
    por_local.reset_index(),
    x="local",
    y="aproveitamento",
    text="aproveitamento",
    title="Aproveitamento do Flamengo: casa x fora",
    labels={"local": "Local", "aproveitamento": "Aproveitamento (%)"},
)
grafico.update_yaxes(range=[0, 100])
st.plotly_chart(grafico)

resultados = jogos.groupby(["local", "resultado"]).size().reset_index(name="quantidade")

grafico2 = px.bar(
    resultados,
    x="local",
    y="quantidade",
    color="resultado",
    barmode="group",
    text="quantidade",
    title="Vitórias, empates e derrotas: casa x fora",
    labels={"local": "Local", "quantidade": "Jogos", "resultado": "Resultado"},
    category_orders={"resultado": ["V", "E", "D"]},
    color_discrete_map={"V": "green", "E": "gray", "D": "red"},
)
st.plotly_chart(grafico2)

evolucao = filtrados.copy()
evolucao["pontos_acumulados"] = evolucao["pontos"].cumsum()

st.subheader("Jogos")
st.dataframe(filtrados)
