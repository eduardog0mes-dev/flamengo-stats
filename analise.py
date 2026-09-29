import pandas as pd
import plotly.express as px

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

total_jogos = len(jogos)
total_pontos = jogos["pontos"].sum()
aproveitamento = total_pontos / (total_jogos * 3) * 100
saldo_total = jogos["saldo"].sum()

print("Jogos:", total_jogos)
print("Pontos:", total_pontos)
print(f"Aproveitamento: {aproveitamento:.1f}%")
print("Saldo de gols:", saldo_total)
print(jogos["resultado"].value_counts())

por_local = jogos.groupby("local").agg(
    partidas=("pontos", "count"),
    pontos=("pontos", "sum"),
    saldo=("saldo", "sum"),
)

por_local["aproveitamento"] = (por_local["pontos"] / (por_local["partidas"] * 3) * 100).round(1)

print(por_local)

dados_grafico = por_local.reset_index()

grafico = px.bar(
    dados_grafico,
    x="local",
    y="aproveitamento",
    text="aproveitamento",
    title="Aproveitamento do Flamengo: casa x fora",
    labels={"local": "Local", "aproveitamento": "Aproveitamento (%)"},
)

grafico.update_yaxes(range=[0, 100])

grafico.show()

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

grafico2.show()


