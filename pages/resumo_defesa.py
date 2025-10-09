import streamlit as st
import pandas as pd
import func

st.markdown("""
                <style>
                h1 {color: darkblue !important;
                    text_align: center;
                }
                <style>""", unsafe_allow_html=True)

st.title("RESUMO GERAL DA DEFESA")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])

st.write("")
df_crz, df_adv = func.resumo_defesa(competicoes=competicao_sel, mando=mando_sel)

st.markdown(
    """
    <p style='color:darkblue; text-align:justify;'>
        A FAVOR DO CRUZEIRO
    </p>
    """,
    unsafe_allow_html=True
)
st.table(df_crz)

st.write("")

st.markdown(
    """
    <p style='color:darkblue; text-align:justify;'>
        A FAVOR DO ADVERSÁRIO
    </p>
    """,
    unsafe_allow_html=True
)
st.table(df_adv)