import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title= 'Dashboard', page_icon=":bar_chart:",layout="wide")

# Add a title and intro text
st.title('Biodiversity Metrics Explorer')

def datafile_uploader():
    df = pd.read_csv('4Lenses.csv')
    return df
    
df = datafile_uploader()