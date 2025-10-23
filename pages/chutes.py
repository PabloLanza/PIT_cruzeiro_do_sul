import streamlit as st
import pandas as pd
import func

st.markdown("""
                <style>
                h1 {color: darkblue !important;
                    text_align: center;
                }
                <style>""", unsafe_allow_html=True)

st.title("PAINEL DE FINALIZAÇÕES")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])
st.write("")

daltonico = st.checkbox("Sou Daltônico")

fig1, fig2, fig3, fig4 = func.perfil_finalizacoes(competicoes=competicao_sel, mando=mando_sel, dalt=daltonico)
st.pyplot(fig1)
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")

st.pyplot(fig2)
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")

st.pyplot(fig3)
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")

st.pyplot(fig4)
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")