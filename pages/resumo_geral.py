import streamlit as st
import pandas as pd
import func

st.markdown("""
                <style>
                h1 {color: darkblue !important;
                    text_align: center;
                }
                <style>""", unsafe_allow_html=True)

st.title("RESUMO GERAL")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])
st.write("")
filtro_sel = st.selectbox("Selecione a Estatística: ", ["Posse de Bola", "Chutes", "Chutes ao Gol", "Chutes de Dentro da Área",
                                                         "Chutes de Fora da Área", "Passes", "Passes Certos", "Escanteios", 
                                                         "Faltas Sofridas", "Faltas Cometidas", "Desarmes", "Interceptações", 
                                                         "Recuperações de Bola", "Cortes", "Duelos no Chão Ganhos", "Duelos Aereos Ganhos", 
                                                         "% Duelos no Chão Ganhos", "% Duelos Aéreos Ganhos"])

daltonico = st.checkbox("Sou Daltônico")

fig1 = func.resumo_geral(competicoes=competicao_sel, mando=mando_sel, filtro_grafico=filtro_sel, dalt=daltonico)
st.pyplot(fig1)
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")