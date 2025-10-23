import streamlit as st
import pandas as pd
import func

st.markdown("""
                <style>
                h1 {color: darkblue !important;
                    text_align: center;
                }
                <style>""", unsafe_allow_html=True)

st.title("PAINEL DE ARTILHARIA")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])


#TABELA DE ARTILHEIROS
st.title("Ranking de Artilheiros")
df_gols = func.gols(competicoes=competicao_sel, mando=mando_sel)
st.table(df_gols)
st.download_button("Baixar Excel", data=func.to_excel(df_gols), file_name="dfgols.xlsx")
st.download_button("Baixar CSV", data=df_gols.to_csv(index=False).encode("utf-8"), file_name="dfgols.csv")

comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")

#TABELA DE ASSISTÊNCIAS
st.title("Ranking de Assistências")
df_ass = func.assistencias(competicoes=competicao_sel, mando=mando_sel)
st.table(df_ass)
st.download_button("Baixar Excel", data=func.to_excel(df_ass), file_name="dfass.xlsx")
st.download_button("Baixar CSV", data=df_ass.to_csv(index=False).encode("utf-8"), file_name="dfass.csv")
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")

#TABELA DE PARTICIPAÇÕES EM GOLS
st.title("Ranking de Participações em Gols")
df_participacoes = func.participacoes(competicoes=competicao_sel, mando=mando_sel)
st.table(df_participacoes)
st.download_button("Baixar Excel", data=func.to_excel(df_participacoes), file_name="dfparticipacoes.xlsx")
st.download_button("Baixar CSV", data=df_participacoes.to_csv(index=False).encode("utf-8"), file_name="dfparticipacoes.csv")
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")

#TABELA DE DOBRADINHAS
st.title("Ranking de Dobradinhas")
st.write("Dobradinha é quando um jogador x da assistencias pra um jogador y fazer o gol ou vice-versa")
df_dobradinha = func.dobradinha(competicoes=competicao_sel, mando=mando_sel)
st.table(df_dobradinha)
st.download_button("Baixar Excel", data=func.to_excel(df_dobradinha), file_name="dfdobradinha.xlsx")
st.download_button("Baixar CSV", data=df_dobradinha.to_csv(index=False).encode("utf-8"), file_name="dfdobradinha.csv")
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")

