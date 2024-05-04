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

#Sidebar navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select what you want to display:', 
                           ['Home', 'Data Summary', 'Data Header', 'Scatter Plots', 'Correlations', 'Biodiversity Calculator', 'Metrics Statistics'])

def home():
    st.write('home')
def data_summary():
    st.write('data_summary')
def data_header():
    st.write('data_header')
def scatter_plot():
    st.write('scatter_plot')
def correlation_plot():
    st.write('correlation_plot')
def calc_biodiversity():
    st.write('calc_biodiversity')
def metrics_stats():
    st.write('metrics_stats')

# Navigation options
if options == 'Home':
    home()
elif options == 'Data Summary':
    data_summary()
elif options == 'Data Header':
    data_header()
elif options == 'Scatter Plots':
    scatter_plot()
elif options == 'Correlations':
    correlation_plot()  
elif options == 'Biodiversity Calculator':
    calc_biodiversity()  
elif options == 'Metrics Statistics':
    metrics_stats()  