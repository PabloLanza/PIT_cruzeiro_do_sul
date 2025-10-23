def filtro_comp_mando(c, m, df):
    if len(c) < 1:
        competicoes = ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil']
    else:
        competicoes = c

    
    if len(m) < 1:
        mando = ['Casa', 'Fora']
    else:
        mando = m

    df = df[(df["competicao"].isin(competicoes)) & (df["mando"].isin(mando))]

    return df


def remover_espacos(df):
    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    for col in df.select_dtypes(include=["object", "string"]):
        df[col] = df[col].str.strip()

    return df

def gols(competicoes=[], mando=[]):

    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("bases/escalacoes.xlsx")
    df_jogos = pd.read_excel("bases/jogos.xlsx")

    #JUNÇÃO DOS DFs
    df_gols = pd.merge(df_escalacao[["id_jogo", "autor_gols_pro"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")
    
    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    df_gols = remover_espacos(df=df_gols)

    #CRIANDO UM FILTRO NOS FILTROS
    df_gols = filtro_comp_mando(c=competicoes, m=mando, df=df_gols)    
    
    #REMOVE JOGOS SEM GOLS
    df_gols = df_gols.dropna()


    #QUEBRA AS COLUNAS EM LISTAS
    df_gols["autor_gols_pro"] = df_gols["autor_gols_pro"].str.split(', ')

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_gols = sum(df_gols["autor_gols_pro"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_gols = [item.upper() for item in lista_gols]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "gols": lista_gols
    }

    df_resumo_gols = pd.DataFrame(dados)
    


    #CONTAGEM DE GOLS
    gols = df_resumo_gols["gols"].value_counts().reset_index()

    #RENOMEANDO AS COLUNAS
    gols.columns = ["jogador", "gols"]

    return gols.sort_values(by=("gols"), ascending=False)


def assistencias(competicoes=[], mando=[]):

    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("bases/escalacoes.xlsx")
    df_jogos = pd.read_excel("bases/jogos.xlsx")

    #FAZENDO A JUNÇÃO DOS DFs
    df_ass = pd.merge(df_escalacao[["id_jogo", "assistencias"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")
    
    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    df_ass = remover_espacos(df=df_ass)
    
    #CRIANDO UM FILTRO NOS FILTROS
    df_ass = filtro_comp_mando(c=competicoes, m=mando, df=df_ass)

    #REMOVE JOGOS SEM GOLS
    df_ass = df_ass.dropna()

    #QUEBRA AS COLUNAS EM LISTAS
    df_ass["assistencias"] = df_ass["assistencias"].str.split(', ')

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_ass = sum(df_ass["assistencias"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_ass = [item.upper() for item in lista_ass]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "assistencias": lista_ass
    }

    df_resumo_ass = pd.DataFrame(dados)
    


    #CONTAGEM DE GOLS
    ass = df_resumo_ass["assistencias"].value_counts().reset_index()
    ass.columns = ["jogador", "assistencias"]

    #REMOVENDO COLUNAS COM NONE, PENALTI E FALTA
    ass = ass[~ass["jogador"].isin(["NONE", "PÊNALTI", "FALTA"])]

    return ass.sort_values(by=("assistencias"), ascending=False)


def dobradinha(competicoes=[], mando=[]):
    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("bases/escalacoes.xlsx")
    df_jogos = pd.read_excel("bases/jogos.xlsx")

    #JUNÇÃO DOS DFs
    df_gol_ass = pd.merge(df_escalacao[["id_jogo", "autor_gols_pro", "assistencias"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")

    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    df_gol_ass = remover_espacos(df=df_gol_ass)

    #CRIANDO UM FILTRO NOS FILTROS
    df_gol_ass = filtro_comp_mando(c=competicoes, m=mando, df=df_gol_ass)

    #REMOVENDO COLUNAS QUE NÃO SERÃO USADAS
    df_gol_ass = df_gol_ass[["autor_gols_pro", "assistencias"]]

    #REMOVENDO VALORES NULOS
    df_gol_ass = df_gol_ass.dropna()

    #QUEBRA AS COLUNAS EM LISTAS
    df_gol_ass["autor_gols_pro"] = df_gol_ass["autor_gols_pro"].str.split(', ')
    df_gol_ass["assistencias"] = df_gol_ass["assistencias"].str.split(', ')

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_gol = sum(df_gol_ass["autor_gols_pro"], [])
    lista_ass = sum(df_gol_ass["assistencias"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_gol = [item.upper() for item in lista_gol]
    lista_ass = [item.upper() for item in lista_ass]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "gols": lista_gol,
        "assistencias": lista_ass
    }

    #CRIA O DATA FRAME
    df_dobradinha = pd.DataFrame(dados)

    #INDICA QUE NÃO IMPORTA A ORDEM DA DUPLA (A + B) OU (B + A)
    df_dobradinha["dupla"] = df_dobradinha.apply(lambda x: tuple(sorted([x["gols"], x["assistencias"]])), axis=1)

    #FAZ A CONTAGEM DE QUANTAS VEZES CADA DUPLA APARECEU
    contagem_duplas = df_dobradinha["dupla"].value_counts().reset_index()
    contagem_duplas.columns = ["dupla", "quantidade"]

    #REMOVENDO DADOS NÃO COERENTES
    contagem_duplas = contagem_duplas[contagem_duplas["dupla"].apply(lambda x: all(v not in ["NONE", "PÊNALTI", "FALTA"] for v in x))]

    #TRANFORMAR AS TUPLAS EM STRINGS
    contagem_duplas["dupla"] = contagem_duplas["dupla"].apply(lambda x: " - ".join(map(str, x)))

    return contagem_duplas.sort_values(by="quantidade", ascending=False)


def participacoes(competicoes=[], mando=[]):
    import pandas as pd

    df_gols = gols(competicoes=competicoes, mando=mando)
    df_ass = assistencias(competicoes=competicoes, mando=mando)

    df_participacoes = pd.merge(df_gols, df_ass, on="jogador", how="outer")

    #PREENCHER VALORES AUSENTES COM 0
    df_participacoes = df_participacoes.fillna(0)

    #CALCULA AS PARTICIPACOES (GOLS + ASSISTENCIAS)
    df_participacoes["participacoes"] = df_participacoes["gols"] + df_participacoes["assistencias"]

    #TRANSFORMANDOAS COLUNAS FLOAT DO DF PRO TIPO INT
    for c in df_participacoes.select_dtypes(include="float"):
        df_participacoes[c] = df_participacoes[c].astype(int)
    
    #REMOVENDO DADOS NÃO COERENTES
    df_participacoes = df_participacoes[~df_participacoes["jogador"].isin(["NONE", "PÊNALTI", "FALTA"])]

    return df_participacoes.sort_values(by="participacoes", ascending=False)    
    
    
def perfil_finalizacoes(competicoes=[], mando=[], dalt=False):

    import pandas as pd
    import matplotlib.pyplot as plt

    #TABELAS QUE SERÃO USADAS
    df_jogos = pd.read_excel("bases/jogos.xlsx")
    df_ataque = pd.read_excel("bases/ataque.xlsx")

    #JUNÇÃO DOS DFs
    df_chutes = pd.merge(df_jogos[["id_jogo", "competicao", "mando"]], df_ataque[["id_jogo", "chutes_cruzeiro", "chutes_adv", "chutes_gol_cruzeiro", "chutes_gol_adv", "chutes_area_cruzeiro", "chutes_area_adv", "chutes_fora_area_cruzeiro", "chutes_fora_area_adv"]], on="id_jogo", how="inner")

    #REMOVENDO ESPAÇOS EM COLUNAS STRING
    df_chutes = remover_espacos(df=df_chutes)
    
    #CRIANDO UM FILTRO NOS FILTROS
    df_chutes = filtro_comp_mando(c=competicoes, m=mando, df=df_chutes)
    df_chutes["chutes_nao_gol_cruzeiro"] = df_chutes["chutes_cruzeiro"] - df_chutes["chutes_gol_cruzeiro"]
    df_chutes["chutes_nao_gol_adv"] = df_chutes["chutes_adv"] - df_chutes["chutes_gol_adv"]

    df_chutes_sum = df_chutes[["chutes_cruzeiro", "chutes_adv", "chutes_gol_cruzeiro", "chutes_gol_adv", "chutes_area_cruzeiro", "chutes_area_adv", "chutes_fora_area_cruzeiro", "chutes_fora_area_adv", "chutes_nao_gol_cruzeiro", "chutes_nao_gol_adv"]].sum().reset_index()
    df_chutes_sum.columns = ["stats", "soma"]
    df_chutes_sum["media"] = round(df_chutes_sum["soma"] / len(df_chutes), 0)


    df_chutes_sum = df_chutes_sum.set_index("stats")
    

    #GRAFICO PIZZA CHUTES DENTRO E FORA AREA
    if dalt:
        cores = ["#0038A7", "#eeff00"]
    else:
        cores = ["#0038A7","#67e4f5"]

    valores1 = df_chutes_sum.loc[["chutes_nao_gol_cruzeiro", "chutes_gol_cruzeiro"], "soma"]
    valores2 = df_chutes_sum.loc[["chutes_nao_gol_adv", "chutes_gol_adv"], "soma"]
    valores3 = df_chutes_sum.loc[["chutes_area_cruzeiro", "chutes_fora_area_cruzeiro"], "soma"]
    valores4 = df_chutes_sum.loc[["chutes_area_adv", "chutes_fora_area_adv"], "soma"]

    fig1, ax1 = plt.subplots()
    ax1.pie(valores1,
            labels=["Chutes Sem Direção do Gol", "Chutes Ao Gol"], autopct="%.1f%%", startangle=90, colors=cores,
            wedgeprops={"width": 0.4})
    ax1.set_title("Chutes Sem Direção x Chutes Ao Gol - Cruzeiro", color="#427ef5", fontweight="bold", fontsize=14)
    ax1.set_aspect("equal")

    fig2, ax2 = plt.subplots()
    ax2.pie(valores2,
            labels=["Chutes Sem Direção do Gol", "Chutes Ao Gol"], autopct="%.1f%%", startangle=90, colors=cores,
            wedgeprops={"width": 0.4})
    ax2.set_title("Chutes Sem Direção x Chutes Ao Gol - Adversário", color="#427ef5", fontweight="bold", fontsize=14)
    ax2.set_aspect("equal")

    fig3, ax3 = plt.subplots()
    ax3.pie(valores3, 
            labels=["Dentro da Área", "Fora da Área"], autopct="%.1f%%", startangle=90, colors=cores)
    ax3.set_title("Perfil das Finalizações do Cruzeiro", color="#427ef5", fontweight="bold", fontsize=14)

    fig4, ax4 = plt.subplots()
    ax4.pie(valores4,
            labels=["Dentro da Área", "Fora da Área"], autopct="%.1f%%", startangle=90, colors=cores)
    ax4.set_title("Perfil das Finalizações do Adversário", color="#427ef5", fontweight="bold", fontsize=14)
    plt.tight_layout()

    return fig1, fig2, fig3, fig4
    

def passes_trocados(competicoes=[], mando=[], dalt=False):

    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    #TABELAS QUE SERÃO USADAS
    df_jogos = pd.read_excel("bases/jogos.xlsx")
    df_ataque = pd.read_excel("bases/ataque.xlsx")

    #JUNÇÃO DOS DFs
    df_passes = pd.merge(df_jogos[["id_jogo", "adversario", "competicao", "mando"]], df_ataque[["id_jogo", "passes_cruzeiro", "passes_certos_cruzeiro", "passes_adv", "passes_certos_adv"]], on="id_jogo", how="inner")

    #REMOVENDO ESPAÇOS
    df_passes = remover_espacos(df=df_passes)

    #FILTRO DE COMPETIÇÕES E MANDOS
    df_passes = filtro_comp_mando(c=competicoes, m=mando, df=df_passes)

    #DECLARAÇÃO DAS VARIÁVEIS QUE SERÃO USADAS
    x = df_passes["id_jogo"]
    passes_cruzeiro = df_passes["passes_cruzeiro"]
    passes_certos_cruzeiro = df_passes["passes_certos_cruzeiro"]
    passes_adv = df_passes["passes_adv"]
    passes_certos_adv = df_passes["passes_certos_adv"]

    #GRÁFICOS DE LINHAS
    if dalt:
        cor_crz = "#0038A7"
        cor_adv = "#eeff00"
    else:
        cor_crz = "#0038A7"
        cor_adv = "#67e4f5"
    
    fig1, ax1 = plt.subplots(figsize=(10,5))

    ax1.plot(x, passes_cruzeiro, label="Passes Cruzeiro", marker="o", color=cor_crz)
    ax1.plot(x, passes_adv, label="Passes Adversário", marker="o", color=cor_adv)

    ax1.set_title("Passes Trocados Por Jogo", fontsize=16)
    ax1.legend()
    ax1.set_xlabel("Jogos")
    ax1.set_ylabel("Passes")
    ax1.grid(True)

    fig2, ax2 = plt.subplots(figsize=(10,5))

    ax2.plot(x, passes_certos_cruzeiro, label="Passes Certos Cruzeiro", marker="o", color=cor_crz)
    ax2.plot(x, passes_certos_adv, label="Passes Certos Adversários", marker="o", color=cor_adv)

    ax2.set_title("Passes Certos Por Jogo", fontsize=16)
    ax2.legend()
    ax2.set_xlabel("Jogos")
    ax2.set_ylabel("Passes")
    ax2.grid(True)

    return fig1, fig2
    

def normalizar(val):
    import pandas as pd
    import numpy as np

    #CASO 1 - LISTA JÁ PRONTA
    if isinstance(val, list):
        return [int(x) for x in val if x not in [0, None] and not pd.isna(x)]
    
    elif isinstance(val, str):
        return [int(x) for x in val.split(", ") if x.strip() not in ["", "0"]]

    elif pd.notna(val) and val != 0:
        return [int(val)]
    
    else:
        return []


def minutos_gols(competicoes=[], mando=[], dalt=False):

    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    #TABELAS QUE SERÃO USADAS
    df_esc = pd.read_excel("bases/escalacoes.xlsx")
    df_jogos = pd.read_excel("bases/jogos.xlsx")

    #JUNÇÃO DOS DFs
    df_min = pd.merge(df_esc[["id_jogo", "minutos_gols_pro", "minutos_gols_contra"]], 
                      df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")

    #REMOVENDO ESPAÇOS
    df_min[["competicao", "mando"]] = remover_espacos(df=df_min[["competicao", "mando"]])

    #APLICANDO FILTROS
    df_min = filtro_comp_mando(c=competicoes, m=mando, df=df_min)

    #REMOVENDO AS COLUNAS QUE NÃO SERÃO USADAS
    df_min = df_min[["minutos_gols_pro", "minutos_gols_contra"]]

    #TRANSFORMANDO AS COLUNAS EM LISTAS
    lista_min_gols_pro = df_min["minutos_gols_pro"].apply(normalizar)
    lista_min_gols_contra = df_min["minutos_gols_contra"].apply(normalizar)

    #CONCATENANDO TUDO EM UMA SÓ LISTA
    lista_min_gols_pro = [x for sublist in lista_min_gols_pro for x in sublist]
    lista_min_gols_contra = [x for sublist in lista_min_gols_contra for x in sublist]
    
    #DEFININDO OS INTERVALOS
    bins = list(range(0, 100, 11))

    #CRIAR OS RÓTULOS DOS INTERVALOS
    labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]

    #TRANFORMANDO EM SERIES
    s = pd.Series(lista_min_gols_pro)
    s1 = pd.Series(lista_min_gols_contra)

    #CONTANDO A QUANTIDADE POR INTERVALO
    intervalos_pro = pd.cut(s, bins=bins, labels=labels, right=False).value_counts().sort_index()
    intervalos_contra = pd.cut(s1, bins=bins, labels=labels, right=False).value_counts().sort_index()

    df_pro = intervalos_pro.reset_index()
    df_pro.columns = ["intervalo", "gols_pro"]

    df_contra = intervalos_contra.reset_index()
    df_contra.columns = ["intervalo", "gols_contra"]

    #DF FINAL
    df_final = pd.merge(df_pro, df_contra, on="intervalo", how="inner")

    #PLOT
    intervalos = df_final["intervalo"]
    gols_cruzeiro = df_final["gols_pro"]
    gols_adv = df_final["gols_contra"]

    #LARGURA DAS BARRAS
    largura = 0.35

    #POSIÇÕES NO EIXO X
    x = np.arange(len(intervalos))

    #CRIANDO O GRÁFICO
    if dalt:
        cor_crz = "#0038A7"
        cor_adv = "#eeff00"
    else:
        cor_crz = "#0038A7"
        cor_adv = "#67e4f5"

    fig, ax = plt.subplots(figsize=(10, 6))
    barras1 = ax.bar(x - largura/2, gols_cruzeiro, width=largura, color=cor_crz, label="Gols do Cruzeiro")

    barras2 = ax.bar(x + largura/2, gols_adv, width=largura, color=cor_adv, label="Gols do Adversário")

    ax.set_title("Gols por Intervalo de Minutos", fontsize=16, color="darkblue", fontweight="bold")
    ax.set_xlabel("Intervalo (Minutos)", color="darkblue", fontweight="bold")
    ax.set_ylabel("Gols", color="darkblue", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(intervalos)
    ax.legend()

    ax.bar_label(barras1, padding=3)
    ax.bar_label(barras2, padding=3)

    return fig



def resumo_ataque(competicoes=[], mando=[]):
    import pandas as pd

    #TABELAS QUE SERÃO USADAS
    df_jogos = pd.read_excel("bases/jogos.xlsx")
    df_ataque = pd.read_excel("bases/ataque.xlsx")

    #JUNÇÃO DOS DFs
    df_resumo_ataque = pd.merge(df_jogos[["id_jogo", "competicao", "mando"]], df_ataque, on="id_jogo", how="inner")
    
    #REMOVER ESPAÇOS
    df_resumo_ataque[["competicao", "mando"]] = remover_espacos(df=df_resumo_ataque[["competicao", "mando"]])

    #FILTRO
    df_resumo_ataque = filtro_comp_mando(c=competicoes, m=mando, df=df_resumo_ataque)

    #DIVIDINDO O DF EM CRUZEIRO X ADVERSÁRIO
    df_res_adv = df_resumo_ataque[["posse_adv", "chutes_adv", "chutes_gol_adv", "chutes_area_adv",
                                              "chutes_fora_area_adv", "passes_adv", "passes_certos_adv", "esc_adv"]]
    
    df_resumo_cruzeiro = df_resumo_ataque.drop(["id_jogo", "competicao", "mando", "posse_adv", "chutes_adv", "chutes_gol_adv", "chutes_area_adv",
                                              "chutes_fora_area_adv", "passes_adv", "passes_certos_adv", "esc_adv"], axis=1)


    df_resumo_cruzeiro = round(df_resumo_cruzeiro.mean(), 2).reset_index()
    df_resumo_cruzeiro.columns = ["estatistica", "media por jogo"]
    

    df_res_adv = round(df_res_adv.mean(), 2).reset_index()
    df_res_adv.columns = ["estatistica", "media por jogo"]
    
    
    #ALTERANDO OS NOMES DAS ESTATÍSTICAS
    df_resumo_cruzeiro["estatistica"] = df_resumo_cruzeiro["estatistica"].map({
        "posse_cruzeiro": "Posse de Bola",
        "chutes_cruzeiro": "Chutes",
        "chutes_gol_cruzeiro": "Chutes ao Gol",
        "chutes_area_cruzeiro": "Chutes de Dentro da Área",
        "chutes_fora_area_cruzeiro": "Chutes de Fora da Área",
        "passes_cruzeiro": "Passes",
        "passes_certos_cruzeiro": "Passes Certos",
        "esc_cruzeiro": "Escanteios",
        "lancamentos_cruzeiro": "Lançamentos",
        "lancamentos_cruzeiro_certos": "Lançamentos Certos",
        "cruzamentos_cruzeiro": "Cruzamentos",
        "cruzamentos_cruzeiro_certos": "Cruzamentos Certos"
    })

    df_res_adv["estatistica"] = df_res_adv["estatistica"].map({
        "posse_adv": "Posse de Bola",
        "chutes_adv": "Chutes",
        "chutes_gol_adv": "Chutes ao Gol",
        "chutes_area_adv": "Chutes de Dentro da Área",
        "chutes_fora_area_adv": "Chutes de Fora da Área",
        "passes_adv": "Passes",
        "passes_certos_adv": "Passes Certos",
        "esc_adv": "Escanteios"
    })

    return df_resumo_cruzeiro, df_res_adv


def resumo_defesa(competicoes=[], mando=[]):
    import pandas as pd

    #TABELAS QUE SERÃO USADAS
    df_jogos = pd.read_excel("bases/jogos.xlsx")
    df_defesa = pd.read_excel("bases/defesa.xlsx")

    #JUNÇÃO DOS DFs
    df_resumo_defesa = pd.merge(df_jogos[["id_jogo", "competicao", "mando"]], df_defesa, on="id_jogo", how="inner")

    #REMOVER ESPAÇOS
    df_resumo_defesa[["competicao", "mando"]] = remover_espacos(df=df_resumo_defesa[["competicao", "mando"]])

    #FILTROS
    df_resumo_defesa = filtro_comp_mando(c=competicoes, m=mando, df=df_resumo_defesa)

    #DIVIDINDO O DF EM CRUZEIRO X ADVERSÁRIO
    df_resumo_cruzeiro = df_resumo_defesa.drop(["id_jogo", "competicao", "mando", "desarmes_adv", "int_adv", 
                                                "recup_adv", "cortes_adv"], axis=1)
    df_resumo_adv = df_resumo_defesa[["faltas_sofridas", "faltas_cometidas", "desarmes_adv", "int_adv", "recup_adv", "cortes_adv", "duelos_chao", "duelos_aereos"]]
    df_resumo_adv["duelos_chao_ganhos"] = df_resumo_adv["duelos_chao"] - df_resumo_cruzeiro["duelos_chao_ganhos"]
    df_resumo_adv["duelos_aereos_ganhos"] = df_resumo_adv["duelos_aereos"] - df_resumo_cruzeiro["duelos_aereos_ganhos"]

    #CALCULANDO A % DE DUELOS
    df_resumo_cruzeiro["percent_duelos_chao_ganhos"] = (df_resumo_cruzeiro["duelos_chao_ganhos"] * 100) / df_resumo_cruzeiro["duelos_chao"]
    df_resumo_cruzeiro["percent_duelos_aereos_ganhos"] = (df_resumo_cruzeiro["duelos_aereos_ganhos"] * 100) / df_resumo_cruzeiro["duelos_aereos"]

    df_resumo_adv["percent_duelos_chao_ganhos"] = (df_resumo_adv["duelos_chao_ganhos"] * 100) / df_resumo_adv["duelos_chao"]
    df_resumo_adv["percent_duelos_aereos_ganhos"] = (df_resumo_adv["duelos_aereos_ganhos"] * 100) / df_resumo_adv["duelos_aereos"]

    #REMOVENDO COLUNAS DESNECESSÁRIAS
    df_resumo_cruzeiro = df_resumo_cruzeiro.drop(["duelos_chao", "duelos_aereos"], axis=1)
    df_resumo_adv = df_resumo_adv.drop(["duelos_chao", "duelos_aereos"], axis=1)

    #CALCULANDO A MÉDIA
    df_resumo_cruzeiro = round(df_resumo_cruzeiro.mean(), 2).reset_index()
    df_resumo_cruzeiro.columns = ["estatistica", "media por jogo"]

    df_resumo_adv = round(df_resumo_adv.mean(), 2).reset_index()
    df_resumo_adv.columns = ["estatistica", "media por jogo"]

    #ALTERANDO OS NOMES DAS ESTATÍSTICAS
    df_resumo_cruzeiro["estatistica"] = df_resumo_cruzeiro["estatistica"].map({
        "faltas_sofridas": "Faltas Sofridas",
        "faltas_cometidas": "Faltas Cometidas",
        "desarmes_cruzeiro": "Desarmes",
        "int_cruzeiro": "Interceptações",
        "recup_cruzeiro": "Recuperações de Bola",
        "cortes_cruzeiro": "Cortes",
        "duelos_chao_ganhos": "Duelos no Chão Ganhos",
        "duelos_aereos_ganhos": "Duelos Aereos Ganhos",
        "percent_duelos_chao_ganhos": "% Duelos no Chão Ganhos",
        "percent_duelos_aereos_ganhos": "% Duelos Aéreos Ganhos"
    })

    df_resumo_adv["estatistica"] = df_resumo_adv["estatistica"].map({
        "faltas_sofridas": "Faltas Cometidas",
        "faltas_cometidas": "Faltas Sofridas",
        "desarmes_adv": "Desarmes",
        "int_adv": "Interceptações",
        "recup_adv": "Recuperações de Bola",
        "cortes_adv": "Cortes",
        "duelos_chao_ganhos": "Duelos no Chão Ganhos",
        "duelos_aereos_ganhos": "Duelos Aereos Ganhos",
        "percent_duelos_chao_ganhos": "% Duelos no Chão Ganhos",
        "percent_duelos_aereos_ganhos": "% Duelos Aéreos Ganhos"
    })

    return df_resumo_cruzeiro, df_resumo_adv


def resumo_geral(competicoes=[], mando=[], filtro_grafico="Posse de Bola", dalt=False):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    #QUAIS SÃO AS ESTATÍSTICAS PRINCIPAIS A SEREM MOSTRADAS AQUI?

    #TABELAS QUE SERÃO USADAS
    df_resumo_ataque_cruzeiro, df_resumo_ataque_adv = resumo_ataque(competicoes=competicoes, mando=mando)
    df_resumo_defesa_cruzeiro, df_resumo_defesa_adv = resumo_defesa(competicoes=competicoes, mando=mando)

    #PRIMEIRO GRÁFICO (PIZZA = TERÁ UM FILTRO DA ESTATÍSTICA A SER MOSTRADA AQUI)
    if filtro_grafico in ["Posse de Bola", "Chutes", "Chutes ao Gol", "Chutes de Dentro da Área", "Chutes de Fora da Área", "Passes", "Passes Certos", "Escanteios"]:
        media_cruzeiro = df_resumo_ataque_cruzeiro.loc[df_resumo_ataque_cruzeiro["estatistica"] == filtro_grafico, "media por jogo"].values[0]
        media_adv = df_resumo_ataque_adv.loc[df_resumo_ataque_adv["estatistica"] == filtro_grafico, "media por jogo"].values[0]
    
    else:
        media_cruzeiro = df_resumo_defesa_cruzeiro.loc[df_resumo_defesa_cruzeiro["estatistica"] == filtro_grafico, "media por jogo"].values[0]
        media_adv = df_resumo_defesa_adv.loc[df_resumo_defesa_adv["estatistica"] == filtro_grafico, "media por jogo"].values[0]

    if dalt:
        cores = ["#0038A7", "#eeff00"]
    else:
        cores = ["#0038A7","#67e4f5"]
        
    valores = [media_cruzeiro, media_adv]
    fig1, ax1 = plt.subplots()
    wedges, texts = ax1.pie(valores, 
            labels=["Cruzeiro", "Adversário"], startangle=90, colors=cores)
    
    for i, wedge in enumerate(wedges):
        ang = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
        x = wedge.r * 0.6 * np.cos(np.deg2rad(ang))
        y = wedge.r * 0.6 * np.sin(np.deg2rad(ang))
        ax1.text(x, y, f"{valores[i]}", ha="center", fontsize=10)

    ax1.set_title(f" Média por Jogo de {filtro_grafico}", color="#002266", fontweight="bold", fontsize=14)
    
    return fig1


def to_excel(df):
    from io import BytesIO
    import pandas as pd
    
    output = BytesIO()
    # Usa o openpyxl, que é o engine padrão do pandas
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")
    return output.getvalue()


def mostrar_filtro(c, m):
    if len(c) < 1:
        comp = ["Mineiro", "Sul Americana", "Brasileiro", "Copa do Brasil"]
    else:
        comp = c
    if len(m) < 1:
        man = ["Casa", "Fora"]
    else:
        man = m
    
    return comp, man