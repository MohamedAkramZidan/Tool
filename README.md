
# Project: Population Insights - Data Overview

## 👥 Team Name
**Null Value**

## 📌 Project Title
**Population Insights**

## 🌐 Data Sources
- **First CSV**: [Worldometers - World Population Data (2025 Projections)](https://www.worldometers.info/world-population)
- **Second CSV**: [Worldometers - Yearly Population Data (1955-2050)](https://www.worldometers.info/world-population/population-by-year)

## 📊 Type of Data

### **First CSV: World Population Data (2025 Projections)**
This dataset contains global and country-specific population indicators for the year 2025:
- **Total Population (2025 projection)**
- **Yearly Change (%)**
- **Population Density (P/Km²)**
- **Urban Population (%)**
- **Migrants (net)**
- **Fertility Rate**
- **Median Age**
- **Land Area (Km²)**
- **World Share (%)**

### **Second CSV: Yearly Population Data (1955-2050)**
This dataset includes historical population data and projections from 1955 to 2050:
- **Year (1 July)**
- **Population (Total)**
- **Yearly % Change**
- **Population Density (P/Km²)**
- **Fertility Rate**
- **Median Age**
- **Urban Population (%)**

## 🎯 Project Goal
To analyze and visualize population data projections for 2025 and historical population trends from 1955 to 2050. This will help compare countries and continents across various indicators and enable insights into global population patterns. The dashboard will allow dynamic exploration of population trends, growth rates, fertility rates, and urbanization.

## 🛠️ Tools and Libraries
- **Frontend:** Streamlit
- **Data Processing:** Pandas, Regex
- **Web Scraping:** Requests, BeautifulSoup
- **Visualization:** Matplotlib, Seaborn, GeoPandas
- **Mapping:** Shapefiles from Natural Earth (for geographic plots)

## 🧪 Methodology
### 1. Data Scraping and Storage
- **Web Scraping:** 
    - Use `requests` and `BeautifulSoup` to scrape population data from the Worldometer site.
    - The data will be scraped from tables that provide population statistics by country and continent.
    
- **Storing Data:**
    - After scraping, the data will be processed and stored into two separate CSV files

### 2. Data Loading and Cleaning
- Load the population datasets from the two CSVs
- Clean and preprocess the data to handle special characters, commas, percentages, and Unicode minus signs
- Separate data into continents and countries for the 2025 dataset
- Handle missing values and convert data types appropriately for both datasets

### 3. Data Analysis
- Generate summary statistics for the population, growth rate, density, fertility rate, and more
- Analyze data for patterns or anomalies, especially focusing on the differences between 2025 projections and historical trends

### 4. Visualizations
- Create visualizations for the top 10 countries by different indicators (e.g., population, growth, density) for 2025 projections
- Create line plots of global population over time (1955-2050)
- Create a choropleth map of population density for the 2025 data
- Provide insights into yearly trends, including percentage change and fertility rate
- Generate correlation plots to understand the relationships between various population indicators

### 5. Data Storage
- **Database Storage (MongoDB):**
    - After cleaning and processing the data, the final dataset will be stored in a MongoDB database for easy access and real-time querying.
    - The population data will be divided into two collections in the database:
      - **`countries_population`**: Stores the country-specific population data, with fields like `country_name`, `population_2025`, `yearly_change`, `density`, `fertility_rate`, etc.
      - **`continents_population`**: Stores the continent-level aggregated data, with fields like `continent_name`, `total_population`, `avg_density`, `avg_fertility_rate`, etc.
      - **`Yearly Population Data (1955-2050)`**: includes historical population data and projections from 1955 to 2050.
    
    MongoDB will provide scalability and allow quick retrieval of large datasets, especially useful for our dashboard and data analysis needs.
    
    We will use `pymongo` to interact with MongoDB from Python.
    
### 6. Dashboard Features
- Sidebar navigation menu
- Pages for home, data preview, dashboards, maps, and in-depth analysis
- Dynamic Matplotlib and Seaborn plots rendered inside Streamlit

## 📈 Outputs
- Cleaned datasets for both 2025 projections and historical population data (1955-2050)
- Dashboard with interactive plots for comparing countries and continents
- Map showing global population density for the 2025 dataset
- Correlation and regression analysis for population growth, fertility rates, and density trends

---

🚀 _This project will evolve further with more interactivity and deeper insights as we continue through Phase 2!_
