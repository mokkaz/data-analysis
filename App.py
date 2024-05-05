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
    st.markdown('This is a web app to allow exploration insights into the environmental impact of financial investments')

    st.page_link("pages/Report.py", label="Report", icon="📋")
    st.page_link("pages/Tech Report.py", label="Technical Report", icon="📋")
    st.markdown('''Summary of the Work Done:  
                - The goal of the research was to assess biodiversity impact for informed investment decisions, focusing on biodiversity metrics for a comprehensive evaluation.  
                - Diverse datasets were managed, and additional data sources were identified to develop a universal metric for measuring impact.  
                - The research evaluated assigned datasets, conducted regression analysis using a subset of datasets due to limited data availability, and calculated the margin of error for the results.  
                - A biodiversity score was developed to quantify the impact of biodiversity on health, nutrition, soil quality, pesticide use, and pest management, emphasizing the importance of biodiversity in traditional medicine availability.  
                - The study highlighted that higher biodiversity scores correlate with lower risks to a country's biodiversity, showcasing the significance of maintaining biodiversity for various ecological and health-related benefits .''')
    st.header('Begin exploring the data using the menu on the left')

def data_summary():
    st.header('Statistics of Dataframe')
    st.write(df.describe())

def data_header():
    st.header('Header of Dataframe')
    st.write(df.head())

def scatter_plot():
    st.markdown('A scatter plot identifies a possible relationship between changes observed in two different sets of variables. It provides a visual and statistical means to test the strength of a relationship between two variables.')
    col1, col2 = st.columns(2)
    
    x_axis_val = col1.selectbox('Select the X-axis', options=df.columns)
    y_axis_val = col2.selectbox('Select the Y-axis', options=df.columns)

    plot = px.scatter(df, x=x_axis_val, y=y_axis_val)
    st.plotly_chart(plot, use_container_width=True)

def correlation_plot():
    st.markdown('The Pearson correlation measures the strength of the linear relationship between two variables. It has a value between -1 to 1, with a value of -1 meaning a total negative linear correlation, 0 being no correlation, and + 1 meaning a total positive correlation.')
    corr_selected = st.multiselect('Choose the metrics to have the corresponding correlation heatmap:', 
                                   options=df.columns,
                                   default=list(df.columns))
    corr = df[corr_selected].corr()

    plot = px.imshow(corr, text_auto=True, aspect="auto")
    st.plotly_chart(plot, use_container_width=True)

def calc_biodiversity():
    col1, col2, col3 , col4 = st.columns(4)
    x1= col1.number_input(label='Agricultural land (% of land area)')
    x2= col2.number_input(label='Forest area (% of land area)')
    x3= col3.number_input(label='Wheat Yield (tonnes/km2)')
    biodiversity_score = -187.3967 - 1.3534*x1 + 10.9765*x2- 32.0721*x3
    col4.text('Biodiversity Score')
    if((x1 != 0) or (x2 != 0) or (x3 != 0)):
        col4.text(biodiversity_score)

    st.divider()
    col5, col6 = st.columns(2)    
    col5.write('\n')
    col5.markdown('You can upload a CSV File with several data point with the metrics corresponding to the calculation of biodiversity.')
    uploaded_file = col5.file_uploader('Upload the CSV file with four column in the following order: Country or Year, Agricultural land (% of land area),  Forest area (% of land area), Wheat Yield (tonnes/km2)')
    if(uploaded_file):
        new_df = pd.read_csv(uploaded_file)
        if(len(new_df.columns) == 4):
            col6.markdown('## Biodiveristy Score:')

            new_df['Biodiversity Score'] = -187.3967 - 1.3534*new_df.iloc[:, 1] + 10.9765*new_df.iloc[:, 2]- 32.0721*new_df.iloc[:, 3]
            col6.write(new_df.iloc[:, [0,-1]])

def metrics_stats():
    selected_page = st.selectbox("Select a page", ["Agricultural Land Data Insights", "Tree Cover Loss Insights", "Deforestation CO2 Trade Insights", "Forest Area Insights", "GHG emissions /kg produced", "Living Planet Index", "Wheat Yields"])

    if(selected_page=='Agricultural Land Data Insights'):
        st.markdown('### Agricultural Land Data Insights:  \nDisplayed trends in agricultural land usage over time for different countries, aiding in understanding agricultural practices globally.  \nCompare the agricultural land percentage across countries to identify regions with significant agricultural activity.')
        df_agri = pd.read_csv('data/Agricultural Land.csv')
        year = st.slider(min_value=1961, max_value=2021, label='Select Year')
        countries = st.multiselect(placeholder='All are Selected. Choose countries for limiting the countries list.', options=df_agri['Country Name'].to_list(), label='Selected Countries:', key='agri_countries')
        if(len(countries) == 0):
            df_selected_countries = df_agri
        else:
            df_selected_countries = df_agri.loc[df_agri['Country Name'].isin(countries)]
        
        selected_years = df_selected_countries[df_selected_countries.columns[pd.Series(df_selected_countries.columns).str.startswith(str(year))]]
        selected_countries = df_selected_countries['Country Name'].to_list()
        
        hist_plot = px.histogram(x=selected_countries, y= selected_years.iloc[:,0].to_list(), labels={'x':'Countries', 'y':'Agricultural Land %'})
        st.plotly_chart(hist_plot, use_container_width=True)
        st.divider()
    
    

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