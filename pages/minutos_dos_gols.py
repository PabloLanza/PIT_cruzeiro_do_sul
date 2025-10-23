import streamlit as st
import pandas as pd
import func

st.markdown("""
                <style>
                h1 {color: darkblue !important;
                    text_align: center;
                }
                <style>""", unsafe_allow_html=True)

st.title("PAINEL DE GOLS POR MINUTO")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])

daltonico = st.checkbox("Sou Daltônico")

fig = func.minutos_gols(competicoes=competicao_sel, mando=mando_sel, dalt=daltonico)

st.pyplot(fig)
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")