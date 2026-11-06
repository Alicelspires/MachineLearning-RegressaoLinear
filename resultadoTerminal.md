```

=== 1 Carregar os dados ===
   dia  publicidade  desconto  vendas
0    1          530        20     214
1    2          190         5     101
2    3          110        20     115
3    4          420        20     181
4    5          280        20     150
Linhas e colunas: (60, 4)
Ausentes por coluna:
dia            0
publicidade    0
desconto       0
vendas         0
dtype: int64

=== 2 Separar os períodos ===
Treino: 40
Validação: 10
Teste: 10

=== 3 Treinar o modelo A ===
Valor inicial: 55.70436504736624
Peso da publicidade: 0.2478042518328812

=== 4 Treinar o modelo B ===
Valor inicial: 32.395810551331465
Pesos das entradas:
publicidade    0.224059
desconto       3.009660
dtype: float64

=== 5 Gerar previsões comparáveis ===
 dia  vendas  previsao_a  previsao_b
  41     183      187.04      181.24
  42     152      144.91      158.20
  43      58       90.40       63.76
  44     104      132.52      116.90
  45     100      112.70       98.98
  46     166      162.26      158.84
  47     192      184.56      194.05
  48      97       80.48       84.90
  49     169      137.48      166.53
  50     135      135.00      134.19

=== 6 Calcular os erros e a média ===
 dia  vendas  previsao_a  previsao_b  erro_a  erro_b  abs_a  abs_b
  41     183      187.04      181.24    4.04   -1.76   4.04   1.76
  42     152      144.91      158.20   -7.09    6.20   7.09   6.20
  43      58       90.40       63.76   32.40    5.76  32.40   5.76
  44     104      132.52      116.90   28.52   12.90  28.52  12.90
  45     100      112.70       98.98   12.70   -1.02  12.70   1.02
  46     166      162.26      158.84   -3.74   -7.16   3.74   7.16
  47     192      184.56      194.05   -7.44    2.05   7.44   2.05
  48      97       80.48       84.90  -16.52  -12.10  16.52  12.10
  49     169      137.48      166.53  -31.52   -2.47  31.52   2.47
  50     135      135.00      134.19    0.00   -0.81   0.00   0.81
Erro absoluto médio A: 14.40 unidades
Erro absoluto médio B: 5.22 unidades
Conferência pela média:
abs_a    14.396111
abs_b     5.224232
dtype: float64

=== 7 Visualizar e escolher ===
Modelo escolhido na validação: B

=== 8 Avaliar o modelo escolhido no teste ===
 dia  vendas  previsao
  51     171    166.83
  52     145    140.28
  53     128    117.87
  54     101    105.06
  55     154    168.77
  56     154    152.12
  57     133    135.80
  58     105    104.09
  59     141    128.74
  60     127    133.56
Modelo B no teste: 6.23 unidades

=== 9 Fazer uma nova previsão e salvar ===
Venda estimada: 129.71 unidades

```