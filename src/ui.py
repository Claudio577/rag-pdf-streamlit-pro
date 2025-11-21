import streamlit as st

def show_pdf_list(pdf_list):
    st.sidebar.write("PDFs carregados:")
    for pdf in pdf_list:
        st.sidebar.write(f"- {pdf}")
