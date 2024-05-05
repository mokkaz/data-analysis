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
    st.markdown('Following the regression analysis, this score that we have can be used to compare two different countries.  \nHigher scores shows that the country has more forest area and lower wheat yield and agricultural land.Therefore the higher the diversity score, the lower the risk of the country on biodiversity.')
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
    uploaded_file = col5.file_uploader('The CSV file must be with four column in the following order: Country or Year, Agricultural land (% of land area),  Forest area (% of land area), Wheat Yield (tonnes/km2)')
    if(uploaded_file):
        new_df = pd.read_csv(uploaded_file)
        if(len(new_df.columns) == 4):
            if (not new_df.iloc[:, 1:4].apply(pd.to_numeric, errors='coerce').isnull().values.any()):
                col6.markdown('## Biodiveristy Score:')

                new_df['Biodiversity Score'] = -187.3967 - 1.3534*new_df.iloc[:, 1] + 10.9765*new_df.iloc[:, 2]- 32.0721*new_df.iloc[:, 3]
                col6.write(new_df.iloc[:, [0,-1]])
            else:
                col6.write(':red[Make sure you uploaded the right file with the right table structure as mentioned!]')
        else:
            col6.write(':red[Make sure you uploaded the right file with the right table structure as mentioned!]')

def metrics_stats():
    selected_page = st.selectbox("Select a metric", ["Agricultural Land Data Insights", "Tree Cover Loss Insights", "Deforestation CO2 Trade Insights", "Forest Area Insights", "GHG emissions /kg produced", "Living Planet Index", "Wheat Yields"])

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
    
    
    if(selected_page=='Tree Cover Loss Insights'):
        st.markdown('### Tree Cover Loss Insights:  \nDisplayed tree cover loss trends over the years for different countries, highlighting regions experiencing significant deforestation or environmental degradation')
        df_treeloss = pd.read_csv('data/Tree Cover Loss.csv')
        year = st.slider(min_value=2002, max_value=2021, label='Select Year')
        countries = st.multiselect(placeholder='All are Selected. Choose countries for limiting the countries list.', options=df_treeloss['Country Name'].to_list(), label='Selected Countries:', key='coutries_treeloss')
        if(len(countries) == 0):
            df_selected_countries = df_treeloss
        else:
            df_selected_countries = df_treeloss.loc[df_treeloss['Country Name'].isin(countries)]
        
        selected_years = df_selected_countries[df_selected_countries.columns[pd.Series(df_selected_countries.columns).str.startswith(str(year))]]
        selected_countries = df_selected_countries['Country Name'].to_list()
        
        hist_plot = px.histogram(x=selected_countries, y= selected_years.iloc[:,0].to_list(), labels={'x':'Countries', 'y':'Tree Cover Loss'})
        st.plotly_chart(hist_plot, use_container_width=True)
        st.divider()

    if(selected_page=='Deforestation CO2 Trade Insights'):
        st.markdown('### Deforestation CO2 Trade Insights:  \nAnalyzed CO2 emissions, as of 2013, due to deforestation in various agricultural product production countries, providing insights into the environmental impact of different food production processes.')
        df_co2 = pd.read_csv('data/deforestation-co2-trade-by-product.csv')
        product = st.multiselect(placeholder='Select the product',max_selections=1, options=df_co2.columns.to_list()[3:12], label='Selected Products:', key='coutries_co2_prod', default='cattle_meat')
        countries = st.multiselect(placeholder='All are Selected. Choose countries for limiting the countries list.', options=df_co2['Entity'].to_list(), label='Selected Countries:', key='coutries_co2')
        if(len(countries) == 0):
            df_selected_countries = df_co2
        else:
            df_selected_countries = df_co2.loc[df_co2['Entity'].isin(countries)]
        if(len(product) == 0):
            st.write(':red[Please choose a product from the dropdown list above.]')
        else:
            selected_products = df_selected_countries[product[0]].to_list()
            selected_countries = df_selected_countries['Entity'].to_list()
            
            hist_plot = px.histogram(x=selected_countries, y= selected_products, labels={'x':'Countries', 'y':'Deforestation CO2 trade'})
            st.plotly_chart(hist_plot, use_container_width=True)
        st.divider()

    if(selected_page=='Forest Area Insights'):
        st.markdown('### Forest Area Insights:  \nIdentified countries or regions with significant fluctuations in forest area coverage, highlighting areas of concern for conservation efforts.')
        df_forestarea = pd.read_csv('data/Forest Area.csv')
        year = st.slider(min_value=1990, max_value=2021, label='Select Year')
        countries = st.multiselect(placeholder='All are Selected. Choose countries for limiting the countries list.', options=df_forestarea['Country Name'].to_list(), label='Selected Countries:', key='forest_countries')
        if(len(countries) == 0):
            df_selected_countries = df_forestarea
        else:
            df_selected_countries = df_forestarea.loc[df_forestarea['Country Name'].isin(countries)]
        
        selected_years = df_selected_countries[df_selected_countries.columns[pd.Series(df_selected_countries.columns).str.startswith(str(year))]]
        selected_countries = df_selected_countries['Country Name'].to_list()
        
        hist_plot = px.histogram(x=selected_countries, y= selected_years.iloc[:,0].to_list(), labels={'x':'Countries', 'y':'Forest Area %'})
        st.plotly_chart(hist_plot, use_container_width=True)
        st.divider()

    if(selected_page=='GHG emissions /kg produced'):
        st.markdown('### GHG emissions per kilogram produced Insights:  \nEvaluated the greenhouse gas (GHG) emissions per kilogram, as of 2010, of various food products, providing insights into the environmental impact of food production processes.')
        df_forestarea = pd.read_csv('data/GHG emissions per kilogram produced.csv')
        food_products = st.multiselect(placeholder='All are Selected. Choose food products for limiting the food products list.', options=df_forestarea['Entity'].to_list(), label='Selected Food Products:', key='forest_countries')
        if(len(food_products) == 0):
            df_selected_food_products = df_forestarea
        else:
            df_selected_food_products = df_forestarea.loc[df_forestarea['Entity'].isin(food_products)]
        
        selected_col = df_selected_food_products['GHG emissions per kilogram (Poore & Nemecek, 2018)'].to_list()
        selected_food_products = df_selected_food_products['Entity'].to_list()
        
        hist_plot = px.histogram(x=selected_food_products, y= selected_col, labels={'x':'Food Products', 'y':'GHG/kg'})
        st.plotly_chart(hist_plot, use_container_width=True)
        st.divider()

    if(selected_page=='Living Planet Index'):
        st.markdown('### Living Planet Index Insights:  \nTracks the variations in vertebrate populations of various species globally from 1970 to the most recent year available, offering a comprehensive view of biodiversity changes.  \n')
        df_LPI = pd.read_csv('data/global-living-planet-index.csv')
        
        col1, col2 = st.columns(2)
        country = col1.multiselect(placeholder='Select an Entity.', options=df_LPI['Entity'].drop_duplicates().to_list(), label='Selected Region:', key='country_lpi', default='World', max_selections=1)
        
        if(len(country) == 0):
            col1.write(':red[Choose an entity from the dropdown list above]')
        else:
            selected_country = df_LPI.loc[df_LPI['Entity'] == country[0]]

            x = selected_country['Year']
            lpi = selected_country['Living Planet Index']
            upper_ci = selected_country['Upper CI']
            lower_ci = selected_country['Lower CI']

            plt.figure(figsize=(5,3))
            plt.plot(x, lpi, 'g', label='Living Planet Index')
            plt.plot(x, upper_ci, 'r', label='Upper CI')
            plt.plot(x, lower_ci, 'y', label='Lower CI')
            plt.legend()
            col1.pyplot(plt.gcf())

        year = col2.multiselect(placeholder='Select a year.', options=df_LPI['Year'].drop_duplicates().to_list(), label='Selected Year:', key='year_lpi', default=2018, max_selections=1)
        if(len(year) == 0):
            col2.write(':red[Choose a year from the dropdown list above]')
        else:
            selected_year = df_LPI.loc[df_LPI['Year'] == year[0]]

            countries = selected_year['Entity'].tolist()
            lpi = selected_year['Living Planet Index'].tolist()

            hist_plot = px.histogram(x=countries, y= lpi, labels={'x':'Countries', 'y':'LPI'})
            col2.plotly_chart(hist_plot, use_container_width=True)

        st.divider()

    if(selected_page=='Wheat Yields'):
        st.markdown('### Wheat Yields Insights:  \nHigher wheat yields often require more land for cultivation, potentially leading to increased deforestation and habitat loss.  \n')
        df_LPI = pd.read_csv('data/wheat-yields.csv')
        
        col1, col2 = st.columns(2)
        country = col1.multiselect(placeholder='Select a country.', options=df_LPI['Entity'].drop_duplicates().to_list(), label='Selected Country:', key='country_wy', default='World', max_selections=1)
        if(len(country) == 0):
            col1.write(':red[Choose an entity from the dropdown list above]')
        else:
            selected_country = df_LPI.loc[df_LPI['Entity'] == country[0]]

            x = selected_country['Year']
            wheat_yield = selected_country['Wheat yield']

            plt.figure(figsize=(5,3))
            plt.plot(x, wheat_yield, 'b', label='Wheat Yield')
            plt.legend()
            col1.pyplot(plt.gcf())

        year = col2.multiselect(placeholder='Select a year.', options=df_LPI['Year'].drop_duplicates().to_list(), label='Selected Year:', key='year_wy', default=2018, max_selections=1)
        if(len(year) == 0):
            col2.write(':red[Choose a year from the dropdown list above]')
        else:
            selected_year = df_LPI.loc[df_LPI['Year'] == year[0]]

            countries = selected_year['Entity'].tolist()
            wy = selected_year['Wheat yield'].tolist()

            hist_plot = px.histogram(x=countries, y= wy, labels={'x':'Countries', 'y':'Wheat yield'})
            col2.plotly_chart(hist_plot, use_container_width=True)

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
     
