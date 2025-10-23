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
st.download_button("Baixar Excel", data=func.to_excel(df_crz), file_name="dfcrz.xlsx")
st.download_button("Baixar CSV", data=df_crz.to_csv(index=False).encode("utf-8"), file_name="dfcrz.csv")
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")

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
st.download_button("Baixar Excel", data=func.to_excel(df_adv), file_name="dfadv.xlsx")
st.download_button("Baixar CSV", data=df_adv.to_csv(index=False).encode("utf-8"), file_name="dfadv.csv")
comp, man = func.mostrar_filtro(competicao_sel, mando_sel)
st.write(f"Filtros Utilizados: Competições - {comp} / Mandos - {man}")