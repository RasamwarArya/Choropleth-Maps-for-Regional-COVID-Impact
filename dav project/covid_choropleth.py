"""
COVID-19 Choropleth Map Visualization using Matplotlib
Fetches real data from online sources and creates interactive visualizations
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import geopandas as gpd
from shapely.geometry import Point
import warnings
warnings.filterwarnings('ignore')

class COVIDChoroplethMap:
    def __init__(self):
        self.covid_data = None
        self.world_data = None
        self.country_mapping = {}
        self.setup_country_mapping()
        
    def setup_country_mapping(self):
        """Map country names between different data sources"""
        self.country_mapping = {
            'US': 'United States of America',
            'USA': 'United States of America',
            'United States': 'United States of America',
            'UK': 'United Kingdom',
            'United Kingdom': 'United Kingdom',
            'South Korea': 'South Korea',
            'Korea, South': 'South Korea',
            'Russia': 'Russia',
            'Russian Federation': 'Russia',
            'Iran': 'Iran',
            'Iran, Islamic Republic of': 'Iran',
            'UAE': 'United Arab Emirates',
            'United Arab Emirates': 'United Arab Emirates',
            'Czech Republic': 'Czech Republic',
            'Czechia': 'Czech Republic',
            'Slovakia': 'Slovakia',
            'Slovak Republic': 'Slovakia',
            'Moldova': 'Moldova',
            'Republic of Moldova': 'Moldova',
            'North Macedonia': 'North Macedonia',
            'Macedonia': 'North Macedonia',
            'Bosnia and Herzegovina': 'Bosnia and Herzegovina',
            'Bosnia': 'Bosnia and Herzegovina',
            'Venezuela': 'Venezuela',
            'Venezuela, Bolivarian Republic of': 'Venezuela',
            'Bolivia': 'Bolivia',
            'Bolivia, Plurinational State of': 'Bolivia',
            'Dominican Republic': 'Dominican Republic',
            'Honduras': 'Honduras',
            'Guatemala': 'Guatemala',
            'Costa Rica': 'Costa Rica',
            'Panama': 'Panama',
            'El Salvador': 'El Salvador',
            'Nicaragua': 'Nicaragua',
            'Jamaica': 'Jamaica',
            'Haiti': 'Haiti',
            'Cuba': 'Cuba',
            'Trinidad and Tobago': 'Trinidad and Tobago',
            'Barbados': 'Barbados',
            'Bahamas': 'Bahamas',
            'Belize': 'Belize',
            'Guyana': 'Guyana',
            'Suriname': 'Suriname',
            'Paraguay': 'Paraguay',
            'Uruguay': 'Uruguay',
            'Chile': 'Chile',
            'Peru': 'Peru',
            'Ecuador': 'Ecuador',
            'Colombia': 'Colombia',
            'Brazil': 'Brazil',
            'Argentina': 'Argentina',
            'China': 'China',
            'Japan': 'Japan',
            'India': 'India',
            'Indonesia': 'Indonesia',
            'Thailand': 'Thailand',
            'Vietnam': 'Vietnam',
            'Philippines': 'Philippines',
            'Malaysia': 'Malaysia',
            'Singapore': 'Singapore',
            'Myanmar': 'Myanmar',
            'Cambodia': 'Cambodia',
            'Laos': 'Laos',
            'Bangladesh': 'Bangladesh',
            'Pakistan': 'Pakistan',
            'Sri Lanka': 'Sri Lanka',
            'Nepal': 'Nepal',
            'Bhutan': 'Bhutan',
            'Maldives': 'Maldives',
            'Afghanistan': 'Afghanistan',
            'Kazakhstan': 'Kazakhstan',
            'Uzbekistan': 'Uzbekistan',
            'Kyrgyzstan': 'Kyrgyzstan',
            'Tajikistan': 'Tajikistan',
            'Turkmenistan': 'Turkmenistan',
            'Mongolia': 'Mongolia',
            'North Korea': 'North Korea',
            'Korea, North': 'North Korea',
            'Taiwan': 'Taiwan',
            'Taiwan*': 'Taiwan',
            'Hong Kong': 'Hong Kong',
            'Macau': 'Macau',
            'Macao': 'Macau',
            'Australia': 'Australia',
            'New Zealand': 'New Zealand',
            'Papua New Guinea': 'Papua New Guinea',
            'Fiji': 'Fiji',
            'Samoa': 'Samoa',
            'Tonga': 'Tonga',
            'Vanuatu': 'Vanuatu',
            'Solomon Islands': 'Solomon Islands',
            'Palau': 'Palau',
            'Micronesia': 'Micronesia',
            'Marshall Islands': 'Marshall Islands',
            'Kiribati': 'Kiribati',
            'Tuvalu': 'Tuvalu',
            'Nauru': 'Nauru',
            'Germany': 'Germany',
            'France': 'France',
            'Italy': 'Italy',
            'Spain': 'Spain',
            'Netherlands': 'Netherlands',
            'Belgium': 'Belgium',
            'Switzerland': 'Switzerland',
            'Austria': 'Austria',
            'Sweden': 'Sweden',
            'Norway': 'Norway',
            'Denmark': 'Denmark',
            'Finland': 'Finland',
            'Iceland': 'Iceland',
            'Ireland': 'Ireland',
            'Portugal': 'Portugal',
            'Greece': 'Greece',
            'Turkey': 'Turkey',
            'Poland': 'Poland',
            'Ukraine': 'Ukraine',
            'Romania': 'Romania',
            'Bulgaria': 'Bulgaria',
            'Hungary': 'Hungary',
            'Slovenia': 'Slovenia',
            'Croatia': 'Croatia',
            'Serbia': 'Serbia',
            'Montenegro': 'Montenegro',
            'Albania': 'Albania',
            'Kosovo': 'Kosovo',
            'Estonia': 'Estonia',
            'Latvia': 'Latvia',
            'Lithuania': 'Lithuania',
            'Belarus': 'Belarus',
            'Luxembourg': 'Luxembourg',
            'Malta': 'Malta',
            'Cyprus': 'Cyprus',
            'Israel': 'Israel',
            'Palestine': 'Palestine',
            'Jordan': 'Jordan',
            'Lebanon': 'Lebanon',
            'Syria': 'Syria',
            'Iraq': 'Iraq',
            'Saudi Arabia': 'Saudi Arabia',
            'Kuwait': 'Kuwait',
            'Qatar': 'Qatar',
            'Bahrain': 'Bahrain',
            'Oman': 'Oman',
            'Yemen': 'Yemen',
            'Egypt': 'Egypt',
            'Libya': 'Libya',
            'Tunisia': 'Tunisia',
            'Algeria': 'Algeria',
            'Morocco': 'Morocco',
            'Sudan': 'Sudan',
            'South Sudan': 'South Sudan',
            'Ethiopia': 'Ethiopia',
            'Eritrea': 'Eritrea',
            'Djibouti': 'Djibouti',
            'Somalia': 'Somalia',
            'Kenya': 'Kenya',
            'Uganda': 'Uganda',
            'Tanzania': 'Tanzania',
            'Rwanda': 'Rwanda',
            'Burundi': 'Burundi',
            'Madagascar': 'Madagascar',
            'Mauritius': 'Mauritius',
            'Seychelles': 'Seychelles',
            'Comoros': 'Comoros',
            'Malawi': 'Malawi',
            'Zambia': 'Zambia',
            'Zimbabwe': 'Zimbabwe',
            'Botswana': 'Botswana',
            'Namibia': 'Namibia',
            'South Africa': 'South Africa',
            'Lesotho': 'Lesotho',
            'Swaziland': 'Eswatini',
            'Eswatini': 'Eswatini',
            'Mozambique': 'Mozambique',
            'Angola': 'Angola',
            'Democratic Republic of the Congo': 'Democratic Republic of the Congo',
            'Congo': 'Democratic Republic of the Congo',
            'Central African Republic': 'Central African Republic',
            'Chad': 'Chad',
            'Niger': 'Niger',
            'Nigeria': 'Nigeria',
            'Benin': 'Benin',
            'Togo': 'Togo',
            'Ghana': 'Ghana',
            'Burkina Faso': 'Burkina Faso',
            'Mali': 'Mali',
            'Senegal': 'Senegal',
            'Gambia': 'Gambia',
            'Guinea-Bissau': 'Guinea-Bissau',
            'Guinea': 'Guinea',
            'Sierra Leone': 'Sierra Leone',
            'Liberia': 'Liberia',
            'Ivory Coast': 'Ivory Coast',
            'Cote d\'Ivoire': 'Ivory Coast',
            'Cameroon': 'Cameroon',
            'Equatorial Guinea': 'Equatorial Guinea',
            'Gabon': 'Gabon',
            'Sao Tome and Principe': 'Sao Tome and Principe',
            'Cape Verde': 'Cape Verde',
            'Canada': 'Canada',
            'Mexico': 'Mexico'
        }

    def fetch_covid_data(self, source='jhu'):
        """Fetch COVID-19 data from online sources"""
        print("Fetching COVID-19 data...")
        
        if source == 'jhu':
            return self.fetch_jhu_data()
        elif source == 'owid':
            return self.fetch_owid_data()
        else:
            return self.fetch_sample_data()

    def fetch_jhu_data(self):
        """Fetch data from Johns Hopkins University CSSE"""
        try:
            # JHU CSSE GitHub repository
            url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
            
            # Fetch confirmed cases
            confirmed_df = pd.read_csv(url)
            
            # Get the latest date (last column)
            latest_date = confirmed_df.columns[-1]
            
            # Process the data
            covid_data = {}
            for _, row in confirmed_df.iterrows():
                country = row['Country/Region']
                province = row['Province/State']
                lat = row['Lat']
                lon = row['Long']
                cases = row[latest_date]
                
                # Standardize country name
                country_std = self.country_mapping.get(country, country)
                
                if country_std not in covid_data:
                    covid_data[country_std] = {
                        'cases': 0,
                        'deaths': 0,
                        'recovered': 0,
                        'lat': lat,
                        'lon': lon,
                        'population': 0
                    }
                
                covid_data[country_std]['cases'] += cases
            
            # Fetch deaths data
            deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
            deaths_df = pd.read_csv(deaths_url)
            
            for _, row in deaths_df.iterrows():
                country = row['Country/Region']
                deaths = row[latest_date]
                country_std = self.country_mapping.get(country, country)
                
                if country_std in covid_data:
                    covid_data[country_std]['deaths'] += deaths
            
            # Fetch recovered data
            recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
            try:
                recovered_df = pd.read_csv(recovered_url)
                
                for _, row in recovered_df.iterrows():
                    country = row['Country/Region']
                    recovered = row[latest_date]
                    country_std = self.country_mapping.get(country, country)
                    
                    if country_std in covid_data:
                        covid_data[country_std]['recovered'] += recovered
                print("Successfully loaded recovered data")
            except Exception as e:
                print(f"Warning: Could not fetch recovered data: {e}")
                print("Estimating recovered cases as 90% of cases...")
                # Estimate recovered cases as 90% of total cases (common recovery rate)
                for country in covid_data:
                    covid_data[country]['recovered'] = int(covid_data[country]['cases'] * 0.9)
            
            # Calculate active cases and fix recovered data if needed
            for country in covid_data:
                # If recovered is 0, estimate it
                if covid_data[country]['recovered'] == 0 and covid_data[country]['cases'] > 0:
                    covid_data[country]['recovered'] = int(covid_data[country]['cases'] * 0.9)
                
                covid_data[country]['active'] = max(0, 
                    covid_data[country]['cases'] - 
                    covid_data[country]['deaths'] - 
                    covid_data[country]['recovered']
                )
            
            print(f"Successfully fetched data for {len(covid_data)} countries")
            return covid_data
            
        except Exception as e:
            print(f"Error fetching JHU data: {e}")
            return self.fetch_sample_data()

    def fetch_owid_data(self):
        """Fetch data from Our World in Data"""
        try:
            url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
            df = pd.read_csv(url)
            
            covid_data = {}
            for _, row in df.iterrows():
                country = row['location']
                country_std = self.country_mapping.get(country, country)
                
                cases = int(row['total_cases']) if pd.notna(row['total_cases']) else 0
                deaths = int(row['total_deaths']) if pd.notna(row['total_deaths']) else 0
                population = int(row['population']) if pd.notna(row['population']) else 0
                
                # Calculate recovered and active cases
                # If we have total cases and deaths, estimate recovered as 90% of cases
                recovered = int(cases * 0.9) if cases > 0 else 0
                active = max(0, cases - deaths - recovered)
                
                covid_data[country_std] = {
                    'cases': cases,
                    'deaths': deaths,
                    'recovered': recovered,
                    'active': active,
                    'population': population,
                    'lat': 0,  # OWID doesn't provide coordinates
                    'lon': 0
                }
                
                # Calculate per capita metrics
                if covid_data[country_std]['population'] > 0:
                    covid_data[country_std]['cases_per_million'] = (covid_data[country_std]['cases'] / covid_data[country_std]['population']) * 1000000
                    covid_data[country_std]['deaths_per_million'] = (covid_data[country_std]['deaths'] / covid_data[country_std]['population']) * 1000000
                else:
                    covid_data[country_std]['cases_per_million'] = 0
                    covid_data[country_std]['deaths_per_million'] = 0
            
            print(f"Successfully fetched OWID data for {len(covid_data)} countries")
            return covid_data
            
        except Exception as e:
            print(f"Error fetching OWID data: {e}")
            return self.fetch_sample_data()

    def fetch_sample_data(self):
        """Generate sample data for demonstration"""
        print("Using sample data for demonstration...")
        
        countries = [
            'United States of America', 'China', 'India', 'Brazil', 'Russia',
            'United Kingdom', 'France', 'Germany', 'Italy', 'Spain',
            'Canada', 'Australia', 'Japan', 'South Korea', 'Mexico',
            'Argentina', 'Chile', 'Colombia', 'Peru', 'South Africa',
            'Egypt', 'Nigeria', 'Kenya', 'Morocco', 'Algeria',
            'Saudi Arabia', 'Turkey', 'Iran', 'Iraq', 'Israel',
            'Thailand', 'Vietnam', 'Indonesia', 'Malaysia', 'Philippines',
            'Poland', 'Ukraine', 'Romania', 'Czech Republic', 'Hungary',
            'Netherlands', 'Belgium', 'Switzerland', 'Austria', 'Sweden',
            'Norway', 'Denmark', 'Finland', 'Portugal', 'Greece'
        ]

        covid_data = {}
        for country in countries:
            cases = np.random.randint(10000, 10000000)
            deaths = int(cases * np.random.uniform(0.01, 0.05))
            recovered = int(cases * np.random.uniform(0.7, 0.9))
            population = np.random.randint(1000000, 1000000000)
            
            covid_data[country] = {
                'cases': cases,
                'deaths': deaths,
                'recovered': recovered,
                'active': cases - deaths - recovered,
                'population': population,
                'cases_per_million': (cases / population) * 1000000,
                'deaths_per_million': (deaths / population) * 1000000,
                'lat': np.random.uniform(-60, 60),
                'lon': np.random.uniform(-180, 180)
            }

        return covid_data

    def load_world_data(self):
        """Load world map data"""
        try:
            # Try to load from Natural Earth data using alternative method
            import os
            import urllib.request
            import zipfile
            
            # Check if we already have the world map data
            if os.path.exists("ne_110m_admin_0_countries.shp"):
                world = gpd.read_file("ne_110m_admin_0_countries.shp")
                print("Loaded existing world map data")
                return world
            
            # Try to download from a different source
            print("Downloading world map data...")
            
            # Use a more reliable source for Natural Earth data
            url = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"
            
            try:
                # Download GeoJSON data
                response = urllib.request.urlopen(url)
                geojson_data = response.read()
                
                # Save to file
                with open("world.geojson", "wb") as f:
                    f.write(geojson_data)
                
                # Load the GeoJSON file
                world = gpd.read_file("world.geojson")
                print("Loaded world map data from GeoJSON")
                return world
                
            except Exception as e1:
                print(f"GeoJSON download failed: {e1}")
                
                # Try alternative: download from Natural Earth directly
                url2 = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip"
                
                try:
                    # Set headers to avoid 406 error
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    
                    req = urllib.request.Request(url2, headers=headers)
                    response = urllib.request.urlopen(req)
                    
                    with open("ne_110m_admin_0_countries.zip", "wb") as f:
                        f.write(response.read())
                    
                    # Extract the zip file
                    with zipfile.ZipFile("ne_110m_admin_0_countries.zip", 'r') as zip_ref:
                        zip_ref.extractall(".")
                    
                    # Remove zip file
                    os.remove("ne_110m_admin_0_countries.zip")
                    
                    # Load the shapefile
                    world = gpd.read_file("ne_110m_admin_0_countries.shp")
                    print("Loaded world map data from Natural Earth")
                    return world
                    
                except Exception as e2:
                    print(f"Natural Earth download failed: {e2}")
                    return self.create_simple_world_data()
                    
        except Exception as e:
            print(f"Could not load world map data: {e}")
            return self.create_simple_world_data()

    def create_simple_world_data(self):
        """Create a simplified world map for demonstration"""
        try:
            # Create a simple world map using matplotlib's built-in capabilities
            import matplotlib.patches as patches
            from matplotlib.patches import Rectangle
            
            # Create a simple world map with basic country shapes
            # This is a simplified approach for demonstration
            world_data = {
                'type': 'FeatureCollection',
                'features': []
            }
            
            # Add some basic country shapes (simplified rectangles for major countries)
            countries_shapes = {
                'United States of America': {'bounds': [-125, 25, -66, 49]},
                'China': {'bounds': [73, 18, 135, 54]},
                'India': {'bounds': [68, 6, 97, 37]},
                'Brazil': {'bounds': [-74, -34, -34, 5]},
                'Russia': {'bounds': [19, 41, 180, 82]},
                'Canada': {'bounds': [-141, 42, -52, 84]},
                'Australia': {'bounds': [113, -44, 154, -10]},
                'Germany': {'bounds': [5, 47, 15, 55]},
                'France': {'bounds': [-5, 42, 8, 51]},
                'United Kingdom': {'bounds': [-8, 50, 2, 61]},
                'Italy': {'bounds': [6, 36, 19, 47]},
                'Spain': {'bounds': [-9, 36, 4, 44]},
                'Japan': {'bounds': [129, 31, 146, 46]},
                'South Korea': {'bounds': [125, 33, 132, 39]},
                'Mexico': {'bounds': [-118, 14, -86, 32]},
                'Argentina': {'bounds': [-74, -56, -53, -22]},
                'Chile': {'bounds': [-76, -56, -66, -17]},
                'South Africa': {'bounds': [16, -47, 33, -22]},
                'Egypt': {'bounds': [25, 22, 37, 32]},
                'Nigeria': {'bounds': [3, 4, 15, 14]},
                'Saudi Arabia': {'bounds': [35, 16, 55, 32]},
                'Turkey': {'bounds': [26, 36, 45, 42]},
                'Iran': {'bounds': [44, 25, 64, 40]},
                'Iraq': {'bounds': [38, 29, 49, 37]},
                'Israel': {'bounds': [34, 29, 36, 33]},
                'Thailand': {'bounds': [97, 6, 106, 21]},
                'Vietnam': {'bounds': [102, 8, 110, 23]},
                'Indonesia': {'bounds': [95, -11, 141, 6]},
                'Malaysia': {'bounds': [100, 1, 120, 7]},
                'Philippines': {'bounds': [117, 5, 127, 21]},
                'Poland': {'bounds': [14, 49, 24, 55]},
                'Ukraine': {'bounds': [22, 45, 40, 52]},
                'Romania': {'bounds': [20, 44, 30, 48]},
                'Czech Republic': {'bounds': [12, 49, 19, 51]},
                'Hungary': {'bounds': [16, 46, 23, 49]},
                'Netherlands': {'bounds': [3, 51, 7, 54]},
                'Belgium': {'bounds': [2, 50, 6, 52]},
                'Switzerland': {'bounds': [6, 46, 11, 48]},
                'Austria': {'bounds': [9, 46, 17, 49]},
                'Sweden': {'bounds': [11, 55, 24, 69]},
                'Norway': {'bounds': [4, 58, 31, 71]},
                'Denmark': {'bounds': [8, 55, 15, 58]},
                'Finland': {'bounds': [20, 60, 32, 70]},
                'Portugal': {'bounds': [-9, 37, -6, 42]},
                'Greece': {'bounds': [20, 35, 30, 42]}
            }
            
            for country, shape in countries_shapes.items():
                feature = {
                    'type': 'Feature',
                    'properties': {'name': country},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[
                            [shape['bounds'][0], shape['bounds'][1]],
                            [shape['bounds'][2], shape['bounds'][1]],
                            [shape['bounds'][2], shape['bounds'][3]],
                            [shape['bounds'][0], shape['bounds'][3]],
                            [shape['bounds'][0], shape['bounds'][1]]
                        ]]
                    }
                }
                world_data['features'].append(feature)
            
            # Convert to GeoDataFrame
            import json
            world_gdf = gpd.GeoDataFrame.from_features(world_data['features'])
            print("Created simplified world map data")
            return world_gdf
            
        except Exception as e:
            print(f"Could not create simple world data: {e}")
            return None

    def create_choropleth_map(self, data_type='cases', color_scheme='Reds', figsize=(15, 10)):
        """Create a choropleth map using matplotlib"""
        
        # Load data
        if self.covid_data is None:
            self.covid_data = self.fetch_covid_data()
        
        if self.world_data is None:
            self.world_data = self.load_world_data()
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=figsize)
        
        # Set up color scheme
        color_schemes = {
            'Reds': plt.cm.Reds,
            'Blues': plt.cm.Blues,
            'Greens': plt.cm.Greens,
            'Purples': plt.cm.Purples,
            'Oranges': plt.cm.Oranges,
            'YlOrRd': plt.cm.YlOrRd,
            'YlGnBu': plt.cm.YlGnBu,
            'RdYlBu_r': plt.cm.RdYlBu_r
        }
        
        cmap = color_schemes.get(color_scheme, plt.cm.Reds)
        
        # Get data values
        values = []
        country_names = []
        
        for country, data in self.covid_data.items():
            if data_type in data and data[data_type] > 0:
                values.append(data[data_type])
                country_names.append(country)
        
        if not values:
            print("No data available for the selected metric")
            return fig, ax
        
        # Normalize values for color mapping
        values = np.array(values)
        norm = plt.Normalize(vmin=values.min(), vmax=values.max())
        
        # Create color map
        colors = cmap(norm(values))
        
        # Plot world map if available
        if self.world_data is not None:
            self.world_data.plot(ax=ax, color='lightgray', edgecolor='white', linewidth=0.5)
        
        # Plot countries with data
        color_index = 0
        for country, data in self.covid_data.items():
            if data_type in data and data[data_type] > 0:
                # Find country in world data
                if self.world_data is not None:
                    # Try different column names for country names
                    country_found = False
                    for col in ['name', 'NAME', 'NAME_EN', 'ADMIN', 'COUNTRY']:
                        if col in self.world_data.columns:
                            country_geom = self.world_data[self.world_data[col] == country]
                            if not country_geom.empty:
                                country_geom.plot(ax=ax, color=colors[color_index], edgecolor='white', linewidth=0.5)
                                color_index += 1
                                country_found = True
                                break
                    
                    # If not found by exact name, try partial matching
                    if not country_found:
                        for col in ['name', 'NAME', 'NAME_EN', 'ADMIN', 'COUNTRY']:
                            if col in self.world_data.columns:
                                # Try to find countries that contain our country name
                                matching_countries = self.world_data[
                                    self.world_data[col].str.contains(country, case=False, na=False)
                                ]
                                if not matching_countries.empty:
                                    matching_countries.plot(ax=ax, color=colors[color_index], edgecolor='white', linewidth=0.5)
                                    color_index += 1
                                    country_found = True
                                    break
                    
                    # If still not found, plot as circle
                    if not country_found and 'lat' in data and 'lon' in data:
                        ax.scatter(data['lon'], data['lat'], 
                                 c=[colors[color_index]], s=100, alpha=0.7, edgecolors='black')
                        color_index += 1
                else:
                    # Plot as circles if no world data
                    if 'lat' in data and 'lon' in data:
                        ax.scatter(data['lon'], data['lat'], 
                                 c=[colors[color_index]], s=100, alpha=0.7, edgecolors='black')
                        color_index += 1
        
        # Customize the plot
        ax.set_title(f'COVID-19 {data_type.replace("_", " ").title()} by Country', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        
        # Add colorbar
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, shrink=0.8, aspect=30)
        cbar.set_label(f'{data_type.replace("_", " ").title()}', fontsize=12)
        
        # Format colorbar ticks
        if values.max() > 1000000:
            cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        elif values.max() > 1000:
            cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.1f}K'))
        
        # Add statistics text
        total_cases = sum(data.get('cases', 0) for data in self.covid_data.values())
        total_deaths = sum(data.get('deaths', 0) for data in self.covid_data.values())
        total_recovered = sum(data.get('recovered', 0) for data in self.covid_data.values())
        
        stats_text = f'Global Statistics:\nTotal Cases: {total_cases:,}\nTotal Deaths: {total_deaths:,}\nTotal Recovered: {total_recovered:,}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        return fig, ax

    def create_multiple_views(self, figsize=(20, 15)):
        """Create multiple views of COVID-19 data"""
        data_types = ['cases', 'deaths', 'recovered', 'active']
        color_schemes = ['Reds', 'Blues', 'Greens', 'Oranges']
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        axes = axes.flatten()
        
        for i, (data_type, color_scheme) in enumerate(zip(data_types, color_schemes)):
            ax = axes[i]
            
            # Get data values
            values = []
            for country, data in self.covid_data.items():
                if data_type in data and data[data_type] > 0:
                    values.append(data[data_type])
            
            if not values:
                ax.text(0.5, 0.5, f'No data for {data_type}', 
                       ha='center', va='center', transform=ax.transAxes)
                continue
            
            # Create color map
            cmap = getattr(plt.cm, color_scheme)
            values = np.array(values)
            norm = plt.Normalize(vmin=values.min(), vmax=values.max())
            colors = cmap(norm(values))
            
            # Plot world map if available
            if self.world_data is not None:
                self.world_data.plot(ax=ax, color='lightgray', edgecolor='white', linewidth=0.3)
            
            # Plot countries
            j = 0
            for country, data in self.covid_data.items():
                if data_type in data and data[data_type] > 0:
                    if self.world_data is not None:
                        country_geom = self.world_data[self.world_data['name'] == country]
                        if not country_geom.empty:
                            country_geom.plot(ax=ax, color=colors[j], edgecolor='white', linewidth=0.3)
                    else:
                        ax.scatter(data['lon'], data['lat'], 
                                 c=[colors[j]], s=50, alpha=0.7, edgecolors='black')
                    j += 1
            
            # Customize subplot
            ax.set_title(f'{data_type.replace("_", " ").title()}', fontsize=14, fontweight='bold')
            ax.set_xlabel('Longitude', fontsize=10)
            ax.set_ylabel('Latitude', fontsize=10)
            
            # Add colorbar
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax, shrink=0.8, aspect=30)
            cbar.set_label(f'{data_type.replace("_", " ").title()}', fontsize=10)
        
        plt.suptitle('COVID-19 Global Impact - Multiple Views', fontsize=18, fontweight='bold')
        plt.tight_layout()
        return fig, axes

    def create_time_series_plot(self, countries=None, figsize=(15, 8)):
        """Create a time series plot for selected countries"""
        if countries is None:
            # Select top 10 countries by cases
            country_cases = [(country, data['cases']) for country, data in self.covid_data.items()]
            country_cases.sort(key=lambda x: x[1], reverse=True)
            countries = [country for country, _ in country_cases[:10]]
        
        fig, ax = plt.subplots(figsize=figsize)
        
        for country in countries:
            if country in self.covid_data:
                data = self.covid_data[country]
                ax.bar(country, data['cases'], alpha=0.7, label=country)
        
        ax.set_title('COVID-19 Cases by Country', fontsize=16, fontweight='bold')
        ax.set_xlabel('Country', fontsize=12)
        ax.set_ylabel('Total Cases', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        
        # Format y-axis
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        return fig, ax

    def print_statistics(self):
        """Print global COVID-19 statistics"""
        if self.covid_data is None:
            print("No data available")
            return
        
        total_cases = sum(data.get('cases', 0) for data in self.covid_data.values())
        total_deaths = sum(data.get('deaths', 0) for data in self.covid_data.values())
        total_recovered = sum(data.get('recovered', 0) for data in self.covid_data.values())
        total_active = sum(data.get('active', 0) for data in self.covid_data.values())
        
        print("\n" + "="*50)
        print("GLOBAL COVID-19 STATISTICS")
        print("="*50)
        print(f"Total Cases: {total_cases:,}")
        print(f"Total Deaths: {total_deaths:,}")
        print(f"Total Recovered: {total_recovered:,}")
        print(f"Total Active: {total_active:,}")
        print(f"Death Rate: {(total_deaths/total_cases*100):.2f}%" if total_cases > 0 else "Death Rate: N/A")
        print(f"Recovery Rate: {(total_recovered/total_cases*100):.2f}%" if total_cases > 0 else "Recovery Rate: N/A")
        
        # Top 10 countries by cases
        country_cases = [(country, data['cases']) for country, data in self.covid_data.items()]
        country_cases.sort(key=lambda x: x[1], reverse=True)
        
        print("\nTop 10 Countries by Total Cases:")
        print("-" * 40)
        for i, (country, cases) in enumerate(country_cases[:10], 1):
            print(f"{i:2d}. {country:<25} {cases:>12,}")

def main():
    """Main function to demonstrate the COVID-19 choropleth map"""
    print("COVID-19 Choropleth Map Visualization")
    print("="*50)
    
    # Create the visualizer
    visualizer = COVIDChoroplethMap()
    
    # Fetch data
    print("\n1. Fetching COVID-19 data...")
    visualizer.covid_data = visualizer.fetch_covid_data('jhu')  # Try JHU first
    
    # Print statistics
    print("\n2. Global Statistics:")
    visualizer.print_statistics()
    
    # Create individual choropleth maps
    print("\n3. Creating choropleth maps...")
    
    # Cases map
    fig1, ax1 = visualizer.create_choropleth_map('cases', 'Reds', (15, 10))
    plt.savefig('covid_cases_map.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Deaths map
    fig2, ax2 = visualizer.create_choropleth_map('deaths', 'Reds', (15, 10))
    plt.savefig('covid_deaths_map.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Multiple views
    print("\n4. Creating multiple views...")
    fig3, axes3 = visualizer.create_multiple_views((20, 15))
    plt.savefig('covid_multiple_views.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Time series plot
    print("\n5. Creating time series plot...")
    fig4, ax4 = visualizer.create_time_series_plot()
    plt.savefig('covid_time_series.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nVisualization complete! Check the generated PNG files.")

if __name__ == "__main__":
    main()
