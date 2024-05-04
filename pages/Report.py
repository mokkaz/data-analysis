import streamlit as st
from streamlit_pdf_viewer import pdf_viewer


def show_report():
    with open('FINAL REPORT.pdf', "rb") as f:
            binary_data = f.read()
    if(binary_data):
        pdf_viewer(input=binary_data,width=900)

st.page_link("app.py", label="Back to App", icon="🏠")
st.write("Report: (Scroll Down 🔻)")
show_report()