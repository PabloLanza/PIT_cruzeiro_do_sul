import streamlit as st
import pandas as pd
import func


# Configurações da página
st.set_page_config(
    page_title="Painel Interativo",
    page_icon="📊",
    layout="centered"
)

# Estilo do título
st.markdown(
    """
    <h1 style='color:darkblue; font-weight:bold; text-align:center;'>
        PAINEL ESTATÍSTICO INTERATIVO
    </h1>
    """,
    unsafe_allow_html=True
)

# Espaçamento
st.write("")

# Descrição principal
st.markdown(
    """
    <p style='font-size:18px; text-align:justify;'>
        Esse é um painel interativo onde você, usuário, pode ter acesso a dados tratados 
        e estatísticas utilizando filtros da sua preferência.
    </p>
    """,
    unsafe_allow_html=True
)

# Segundo parágrafo
st.markdown(
    """
    <p style='font-size:18px; text-align:justify;'>
        Navegue entre as páginas pelo menu ao lado esquerdo.
    </p>
    """,
    unsafe_allow_html=True
)

# Espaçamento
st.write("")

# Exibição da imagem (ajuste o caminho conforme o local do arquivo)
st.image("images/img.jpg", caption="Gabigol e Kaio Jorge - Divulgação Cruzeiro", use_container_width=True)
