import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import geopandas as gpd

st.title("Hi, This is Project Tools\n**'Null Value Team'**")

def show_home():
    st.markdown("""
    This app performs simple webscraping of World Population stats data!
    * **Python libraries:** streamlit, requests, BeautifulSoup, re, pandas, matplotlib, seaborn
    * **Data source:** (https://www.worldometers.info/world-population/&ved=2ahUKEwj3kufd6NKMAxXs8LsIHWKVH_cQFnoECB8QAQ&usg=AOvVaw3YMVazKAtMa5WBnfBu2yOi)
    """)

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("PP.csv")
    data = pd.DataFrame(df)
    # Columns to clean: remove commas and replace Unicode minus (or similar) with '-'
    cols_to_clean = ['Population (2025)', 'Net Change', 'Density (P/Km²)', 'Land Area (Km²)', 'Migrants (net)']
    for col in cols_to_clean:
        data[col] = data[col].astype(str).apply(
            lambda x: re.sub(r',|−', lambda m: '-' if m.group() == '−' else '', x)
        ).astype(float)

    # Clean 'Yearly Change': remove '%' and replace Unicode minus with '-'
    data['Yearly Change'] = data['Yearly Change'].astype(str).apply(
        lambda x: re.sub(r'%|−', lambda m: '-' if m.group() == '−' else '', x)
    ).astype(float)

    # Clean 'Urban Pop %': remove '%'
    data['Urban Pop %'] = data['Urban Pop %'].astype(str).apply(
        lambda x: re.sub(r'%', '', x)
    ).astype(float)

    # Clean 'World Share': remove '%'
    data['World Share'] = data['World Share'].astype(str).apply(
        lambda x: re.sub(r'%', '', x)
    ).astype(float)
    return data
data = load_and_clean_data()
def show_clean_data():
    st.title("Clean Data")
    st.success("Data cleaned successfully!")
    st.write(f"**Shape:** {data.shape[0]} rows × {data.shape[1]} columns")

    # Show the cleaned data
    st.subheader("Preview of Cleaned Data")
    st.dataframe(data, use_container_width=True)

def country_df():
    data_country = data.iloc[6:].reset_index(drop=True)
    return data_country
data_country = country_df()

def show_country_data():
    st.title("🌍 Country Data")
    st.write(f"**Countries:** {data_country.shape[0]}")
    st.dataframe(data_country, use_container_width=True)

def continent_df():
    data_continent = data.iloc[:6].reset_index(drop=True)
    return data_continent
data_continent = continent_df()

def show_continent_data():
    st.title("🗺️ Continent Data")
    st.write(f"**Continents:** {data_continent.shape[0]}")
    st.dataframe(data_continent, use_container_width=True)

def show_more_info():
    st.title("📊 More Info")
    st.subheader("🔍 Data Types and Shape")
    st.write(data.dtypes)
    st.write(f"**Shape:** {data.shape[0]} rows × {data.shape[1]} columns")
    st.subheader("🔍 Info")
    buffer = StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()

    st.text(s)

    st.subheader("📈 Statistical Summary")
    st.dataframe(data.describe(), use_container_width=True)

    st.subheader("🧾 Columns")
    st.write(list(data.columns))

    st.subheader("⚠️ Missing Values")
    st.write(data.isnull().sum())

def show_dashboard():
    st.title("📊 Dashboard: Top 10 Countries by Population Indicators")

    # Get top 10 countries by each metric
    top_population = data_country.sort_values('Population (2025)', ascending=False).head(10)
    top_growth = data_country.sort_values('Yearly Change', ascending=False).head(10)
    top_density = data_country.sort_values('Density (P/Km²)', ascending=False).head(10)
    top_fertility = data_country.sort_values('Fertility Rate', ascending=False).head(10)
    top_urban = data_country.sort_values('Urban Pop %', ascending=False).head(10)

    # Create a 3x2 dashboard of bar plots
    fig, axes = plt.subplots(3, 2, figsize=(18, 15), constrained_layout=True)
    fig.suptitle("Top 10 Countries by Population Indicators (2025)", fontsize=20)

    # Population
    sns.barplot(x='Population (2025)', y='Country', data=top_population, ax=axes[0, 0], hue='Country', palette='Blues_d', legend=False)
    axes[0, 0].set_title("Top 10 Countries by Population")

    # Growth Rate
    sns.barplot(x='Yearly Change', y='Country', data=top_growth, ax=axes[0, 1], hue='Country', palette='Greens_d', legend=False)
    axes[0, 1].set_title("Top 10 Countries by Yearly Growth (%)")

    # Density
    sns.barplot(x='Density (P/Km²)', y='Country', data=top_density, ax=axes[1, 0], hue='Country', palette='Oranges_d', legend=False)
    axes[1, 0].set_title("Top 10 Countries by Population Density")

    # Fertility Rate
    sns.barplot(x='Fertility Rate', y='Country', data=top_fertility, ax=axes[1, 1], hue='Country', palette='Purples_d', legend=False)
    axes[1, 1].set_title("Top 10 Countries by Fertility Rate")

    # Urban Population %
    sns.barplot(x='Urban Pop %', y='Country', data=top_urban, ax=axes[2, 0], hue='Country', palette='Reds_d', legend=False)
    axes[2, 0].set_title("Top 10 Countries by Urban Population (%)")

    # Remove the empty plot (bottom right)
    fig.delaxes(axes[2, 1])

    # Ensure tight layout adjustment
    plt.tight_layout()

    # Show the plot in Streamlit
    st.pyplot(fig)

    st.markdown("""
        Top country by population is => india
    
        by Yearly Growth => Tokelau
        
        by Population Density => Monaco "it's bad"
        
        by Fertility Rate => chad "Stop it chad"
        
        by Urban Population => alot of country is 100%  by more population Hong Kong is 'Hero'""")
def show_land_map():
    st.title("🌍 Land Map - Population Density")

    # Load the shapefile
    world = gpd.read_file('ne_110m_admin_0_countries.shp')

    # Merge country data with population density
    world = world.merge(
        data_country[['Country', 'Density (P/Km²)']],
        how='left',
        left_on='NAME',
        right_on='Country'
    )

    # Plot the map
    fig, ax = plt.subplots(figsize=(15, 10))
    world.plot(
        column='Density (P/Km²)',  # your actual data column
        ax=ax,
        legend=True,
        cmap='Reds',
        missing_kwds={'color': 'lightgrey'},
        legend_kwds={'label': "Population Density (P/Km²)", 'orientation': "vertical"}
    )
    plt.title('World Map - Population Density')

    # Show the map in Streamlit
    st.pyplot(fig)

def show_scatter_plots_and_corr():
    st.title("📊 Scatter Plots and Correlation")

    # Scatter Plot 1: Median Age vs Fertility Rate
    st.subheader("1. Median Age vs Fertility Rate")
    sns.scatterplot(data=data_country, x='Median Age', y='Fertility Rate')
    plt.title('Median Age Vs Fertility Rate')
    plt.xscale('Median Age')
    plt.yscale('Fertility Rate')
    st.pyplot(plt)

    # Correlation between Median Age and Fertility Rate
    st.write("Correlation between Median Age and Fertility Rate:", data_country[['Fertility Rate', 'Median Age']].corr().iloc[0, 1])

    # Scatter Plot 2: Migrants (net) vs Net Change
    st.subheader("2. Migrants (net) vs Net Change")
    sns.scatterplot(data=data_country, x='Migrants (net)', y='Net Change')
    plt.title('Migrants (net) Vs Net Change')
    plt.xscale('Migrants (net)')
    plt.yscale('Net Change')
    st.pyplot(plt)

    # Correlation between Migrants (net) and Net Change
    st.write("Correlation between Migrants (net) and Net Change:", data_country[['Migrants (net)', 'Net Change']].corr().iloc[0, 1])

    # Scatter Plot 3: Land Area (Km²) vs Density (P/Km²)
    st.subheader("3. Land Area (Km²) vs Density (P/Km²)")
    sns.scatterplot(data=data_country, x='Land Area (Km²)', y='Density (P/Km²)')
    plt.title('Land Area (Km²) Vs Density (P/Km²)')
    plt.xscale('Land Area (Km²)')
    plt.yscale('Density (P/Km²)')
    st.pyplot(plt)

    # Correlation between Land Area (Km²) and Density (P/Km²)
    st.write("Correlation between Land Area (Km²) and Density (P/Km²):", data_country[['Land Area (Km²)', 'Density (P/Km²)']].corr().iloc[0, 1])

def show_regex_analysis():
    st.title("🔍 Regex Analysis")

    # Countries with negative yearly change
    negative_growth_country = data_country[data_country['Yearly Change'].astype(str).str.match(r'^-.*')]
    st.subheader("Countries with Negative Yearly Change")
    st.write(negative_growth_country[['Country', 'Yearly Change']])

    # Countries with high yearly change (≥ 3.0%)
    high_growth_country = data_country[data_country['Yearly Change'].astype(str).str.match(r'^[3-9]\.\d+|^[1-9]\d+(\.\d+)?')]
    st.subheader("Countries with High Yearly Change (≥ 3.0%)")
    st.write(high_growth_country[['Country', 'Yearly Change']])

    # Countries with high density (≥ 1000 P/Km²)
    high_density = data_country[data_country['Density (P/Km²)'].astype(str).str.match(r'^[1-9]\d{3,}(\.\d+)?')]
    st.subheader("Countries with High Density (≥ 1000 P/Km²)")
    st.write(high_density[['Country', 'Density (P/Km²)']])

@st.cache_data
def load_and_clean_yearly_population_data():
    # Load the dataset
    df2 = pd.read_csv("PP2.csv")
    data2 = pd.DataFrame(df2)

    # Columns to clean: remove commas, replace Unicode minus (or similar) with '-'
    cols_with_commas = ['Population', 'Yearly Change', 'Density (P/Km²)']
    for col in cols_with_commas:
        data2[col] = data2[col].astype(str).apply(
            lambda x: re.sub(r'[,\−]', lambda m: '-' if m.group() == '−' else '', x)
        ).astype(float)

    # Clean 'Yearly % Change': remove '%' and convert to float
    data2['Yearly % Change'] = data2['Yearly % Change'].astype(str).apply(
        lambda x: re.sub(r'%', '', x)
    ).astype(float)

    # Clean 'Median Age' and 'Fertility Rate': Replace '−' with '-'
    numeric_cols = ['Median Age', 'Fertility Rate']
    for col in numeric_cols:
        data2[col] = data2[col].astype(str).apply(
            lambda x: re.sub(r'−', '-', x)
        ).astype(float)

    return data2

# Load and clean the Yearly Population data
data2 = load_and_clean_yearly_population_data()


def show_more_info_yearly_population_data():
    st.title("📊 More Info: Yearly Population Data")

    # Data Types and Shape
    st.subheader("🔍 Data Types and Shape")
    st.write(data2.dtypes)
    st.write(f"**Shape:** {data2.shape[0]} rows × {data2.shape[1]} columns")

    # Data Info (like data.info())
    st.subheader("🔍 Info")
    buffer = StringIO()
    data2.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    # Statistical Summary
    st.subheader("📈 Statistical Summary")
    st.dataframe(data2.describe(), use_container_width=True)

    # Column Names
    st.subheader("🧾 Columns")
    st.write(list(data2.columns))

    # Missing Values
    st.subheader("⚠️ Missing Values")
    st.write(data2.isnull().sum())

def show_clean_data_Yearly():
    st.title("Clean Data")
    st.success("Data cleaned successfully!")
    st.write(f"**Shape:** {data2.shape[0]} rows × {data2.shape[1]} columns")

    # Show the cleaned data
    st.subheader("Preview of Cleaned Data")
    st.dataframe(data2, use_container_width=True)

def show_analysis_for_yearly_population_data():
    st.title("📊 Analysis For Yearly Population Data")

    # Correlation Matrix
    st.subheader("🔍 Correlation Matrix")
    correlation_matrix = data2[['Yearly % Change', 'Fertility Rate', 'Median Age']].corr()
    st.write(correlation_matrix)

    # Plot: Global Population Over Time (1955-2050)
    st.subheader("🌍 Global Population Over Time")
    plt.figure(figsize=(10, 6))
    plt.plot(data2['Year (1 July)'], data2['Population'] / 1e9, marker='o', color='blue')
    plt.title('Global Population Over Time (1955-2050)')
    plt.xlabel('Year')
    plt.ylabel('Population (Billions)')
    plt.grid(True)
    st.pyplot(plt)

    # Plot: Yearly % Change and Fertility Rate Over Time
    st.subheader("📉 Yearly % Change and Fertility Rate Over Time")
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Yearly % Change
    ax1.plot(data2['Year (1 July)'], data2['Yearly % Change'], marker='o', color='green', label='Yearly % Change')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Yearly % Change (%)', color='green')
    ax1.tick_params(axis='y', labelcolor='green')

    # Create second y-axis for Fertility Rate
    ax2 = ax1.twinx()
    ax2.plot(data2['Year (1 July)'], data2['Fertility Rate'], marker='o', color='purple', label='Fertility Rate')
    ax2.set_ylabel('Fertility Rate', color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')

    # Add title and adjust layout
    plt.title('Yearly % Change and Fertility Rate Over Time (1955-2050)')
    fig.tight_layout()
    plt.grid(True)
    st.pyplot(fig)

def main():
    st.sidebar.header('Sidebar Menu')

    option = st.sidebar.radio(
        "Choose What You Want To see!",
        ["Home", "Clean Data","Country Data","Continent Data","More Info",
         "Dashboard: Top 10 Countries","World Map Density Population",
         "Corr and Scatter plots","Regex Analysis",
         "Clean Data For Yearly Population","More Info: Yearly Population Data",
         "Analysis For Yearly Population Data"
         ]
    )

    match option:
        case "Home":
            show_home()
        case "Clean Data":
            show_clean_data()
        case "More Info":
            show_more_info()
        case "Country Data":
            show_country_data()
        case "Continent Data":
            show_continent_data()
        case "Dashboard: Top 10 Countries":
            show_dashboard()
        case "World Map Density Population":
            show_land_map()
        case "Corr and Scatter plots":
            show_scatter_plots_and_corr()
        case "Regex Analysis":
            show_regex_analysis()
        case "Clean Data For Yearly Population":
            show_clean_data_Yearly()
        case "More Info: Yearly Population Data":
            show_more_info_yearly_population_data()
        case "Analysis For Yearly Population Data":
            show_analysis_for_yearly_population_data()

if __name__ == "__main__":
    main()












