from pathlib import Path
import sys
import matplotlib

if "--sem-janelas" in sys.argv:
    matplotlib.use("Agg")

PASTA = Path(__file__).resolve().parent
SAIDA = PASTA / "resultados"
SAIDA.mkdir(exist_ok=True)




print("\n=== 1 Carregar os dados ===")

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

dados = pd.read_csv(PASTA / "real_estate_price_size_year.csv")

print(dados.head())
print("Linhas e colunas:", dados.shape)
print("Ausentes por coluna:")
print(dados.isna().sum())

colunas_necessarias = ["price", "size", "year"]

if not all(col in dados.columns for col in colunas_necessarias):
    raise ValueError("A base de dados possui colunas inesperadas.")

if dados[colunas_necessarias].isna().any().any():
    raise ValueError("Existem valores ausentes na base de dados.")





print("\n=== 2 Separar os períodos ===")

treino = dados.iloc[:60].copy()
validacao = dados.iloc[60:80].copy()
teste = dados.iloc[80:].copy()

treino["registro"] = treino.index + 1
validacao["registro"] = validacao.index + 1
teste["registro"] = teste.index + 1

print("Treino:", len(treino))
print("Validação:", len(validacao))
print("Teste:", len(teste))

plt.scatter(
    treino["size"],
    treino["price"],
    c=treino["year"]
)

plt.colorbar(label="Ano do imóvel")
plt.xlabel("Tamanho do imóvel (m²)")
plt.ylabel("Preço do imóvel")
plt.title("Dados de treinamento")
plt.tight_layout()

plt.savefig(
    SAIDA / "03_dados_treino_imoveis.png",
    dpi=150,
    bbox_inches="tight"
)

if "--sem-janelas" not in sys.argv:
    plt.show()

plt.close()




print("\n=== 3 Treinar o modelo A ===")

colunas_a = ["size"]

modelo_a = LinearRegression()
modelo_a.fit(treino[colunas_a], treino["price"])

print("Valor inicial:", modelo_a.intercept_)
print("Peso do tamanho:", modelo_a.coef_[0])





print("\n=== 4 Treinar o modelo B ===")

colunas_b = ["size", "year"]

modelo_b = LinearRegression()
modelo_b.fit(treino[colunas_b], treino["price"])

print("Valor inicial:", modelo_b.intercept_)
print("Pesos das entradas:")

print(pd.Series(
    modelo_b.coef_,
    index=colunas_b
))


print("\n=== 5 Gerar previsões comparáveis ===")

previsao_a = modelo_a.predict(validacao[colunas_a])
previsao_b = modelo_b.predict(validacao[colunas_b])

comparacao = validacao[
    ["registro", "price"]
].copy()

comparacao["previsao_a"] = previsao_a
comparacao["previsao_b"] = previsao_b

print(comparacao.round(2).to_string(index=False))




print("\n=== 6 Calcular os erros e a média ===")

comparacao["erro_a"] = (
    previsao_a - validacao["price"]
)

comparacao["erro_b"] = (
    previsao_b - validacao["price"]
)

comparacao["abs_a"] = comparacao["erro_a"].abs()
comparacao["abs_b"] = comparacao["erro_b"].abs()

mae_a = mean_absolute_error(
    validacao["price"],
    previsao_a
)

mae_b = mean_absolute_error(
    validacao["price"],
    previsao_b
)

print(comparacao.round(2).to_string(index=False))

print(f"Erro absoluto médio A: {mae_a:.2f}")
print(f"Erro absoluto médio B: {mae_b:.2f}")

print("Conferência pela média:")
print(comparacao[["abs_a", "abs_b"]].mean())





print("\n=== 7 Visualizar e escolher ===")

grafico = comparacao.set_index("registro")

grafico[
    ["price", "previsao_a", "previsao_b"]
].plot(
    marker="o",
    figsize=(10, 5)
)

plt.xlabel("Registro")
plt.ylabel("Preço do imóvel")
plt.title("Preços reais e previsões na validação")
plt.tight_layout()

plt.savefig(
    SAIDA / "04_comparacao_validacao_imoveis.png",
    dpi=150,
    bbox_inches="tight"
)

if "--sem-janelas" not in sys.argv:
    plt.show()

plt.close()

if mae_a <= mae_b:
    escolhido = modelo_a
    colunas = colunas_a
    nome = "A"
else:
    escolhido = modelo_b
    colunas = colunas_b
    nome = "B"

print("Modelo escolhido na validação:", nome)




print("\n=== 8 Avaliar o modelo escolhido no teste ===")

previsao_teste = escolhido.predict(teste[colunas])

mae_teste = mean_absolute_error(
    teste["price"],
    previsao_teste
)

resultado_teste = teste[
    ["registro", "price"]
].copy()

resultado_teste["previsao"] = previsao_teste
resultado_teste["erro"] = (
    previsao_teste - teste["price"]
)
resultado_teste["erro_absoluto"] = (
    resultado_teste["erro"].abs()
)

print(resultado_teste.round(2).to_string(index=False))

print(f"Modelo {nome} no teste: {mae_teste:.2f}")





print("\n=== 9 Fazer uma nova previsão e salvar ===")

novo_imovel = pd.DataFrame({
    "size": [1000],
    "year": [2015]
})

nova_previsao = escolhido.predict(
    novo_imovel[colunas]
)[0]

print("Tamanho do imóvel:", 1000, "m²")
print("Ano do imóvel:", 2015)
print(f"Preço estimado: {nova_previsao:.2f}")

comparacao.to_csv(
    SAIDA / "comparacao_validacao.csv",
    index=False
)

resultado_teste.to_csv(
    SAIDA / "resultado_teste.csv",
    index=False
)