# COVID-19 Choropleth Map Visualization

A Python application that visualizes the geographical spread and intensity of COVID-19 using choropleth maps with matplotlib. This project fetches real data from online sources and creates comprehensive visualizations.

## Features

- **Real Data Integration**: Fetches live COVID-19 data from multiple sources (JHU, Our World in Data)
- **Interactive Choropleth Maps**: Visualize COVID-19 data across different countries with color-coded intensity
- **Multiple Data Views**: Switch between different metrics (cases, deaths, recovered, active cases, per capita data)
- **Customizable Color Schemes**: Choose from various matplotlib color palettes
- **Comprehensive Analysis**: Global statistics, country comparisons, and data export
- **Error Handling**: Robust fallback to sample data if online sources fail
- **High-Quality Output**: Generate publication-ready PNG files

## Technologies Used

- **Python 3.7+**: Core programming language
- **Matplotlib**: Data visualization and plotting
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **GeoPandas**: Geographic data processing
- **Requests**: HTTP data fetching
- **BeautifulSoup4**: Web scraping capabilities

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or Download** the project files to your local machine
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   python covid_choropleth.py
   ```

### File Structure

```
covid-choropleth-map/
├── covid_choropleth.py    # Main application with COVIDChoroplethMap class
├── example_usage.py       # Example usage and demonstrations
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Usage

### Basic Usage

```python
from covid_choropleth import COVIDChoroplethMap

# Create visualizer instance
visualizer = COVIDChoroplethMap()

# Fetch data from Johns Hopkins University
visualizer.covid_data = visualizer.fetch_covid_data('jhu')

# Create a cases map
fig, ax = visualizer.create_choropleth_map('cases', 'Reds', (15, 10))
plt.show()
```

### Data Sources

The application supports multiple data sources:

1. **Johns Hopkins University (JHU)**: Primary source with confirmed cases, deaths, and recovered data
2. **Our World in Data (OWID)**: Alternative source with population data for per-capita calculations
3. **Sample Data**: Fallback option for demonstration when online sources are unavailable

### Available Metrics

- **Total Cases**: Cumulative confirmed cases
- **Total Deaths**: Cumulative deaths
- **Total Recovered**: Cumulative recovered cases
- **Active Cases**: Currently active cases
- **Cases per Million**: Cases normalized by population
- **Deaths per Million**: Deaths normalized by population

### Color Schemes

Available matplotlib color schemes:
- Reds, Blues, Greens, Purples, Oranges
- YlOrRd, YlGnBu, RdYlBu_r
- And many more matplotlib colormaps

## Examples

### 1. Basic Visualization

```python
# Create a simple cases map
visualizer = COVIDChoroplethMap()
visualizer.covid_data = visualizer.fetch_covid_data('jhu')
fig, ax = visualizer.create_choropleth_map('cases', 'Reds')
plt.show()
```

### 2. Multiple Views

```python
# Create multiple views in one figure
fig, axes = visualizer.create_multiple_views((20, 15))
plt.show()
```

### 3. Custom Analysis

```python
# Print global statistics
visualizer.print_statistics()

# Create time series plot
fig, ax = visualizer.create_time_series_plot()
plt.show()
```

### 4. Data Export

```python
# Export data to CSV
import pandas as pd
data_list = []
for country, data in visualizer.covid_data.items():
    data_list.append({
        'Country': country,
        'Cases': data['cases'],
        'Deaths': data['deaths'],
        'Recovered': data['recovered'],
        'Active': data['active']
    })
df = pd.DataFrame(data_list)
df.to_csv('covid_data.csv', index=False)
```

## Running Examples

The `example_usage.py` file contains comprehensive examples:

```bash
python example_usage.py
```

This will run multiple examples demonstrating:
- Basic usage
- Multiple data sources
- Different metrics
- Custom analysis
- Specific countries
- Data export
- Error handling

## Customization

### Adding New Data Sources

To add a new data source:

1. Create a new method in the `COVIDChoroplethMap` class
2. Follow the pattern of existing `fetch_*_data()` methods
3. Return data in the standard format
4. Add the source to the `fetch_covid_data()` method

### Custom Visualizations

Extend the class with new visualization methods:

```python
def create_custom_plot(self, data_type, custom_params):
    # Your custom visualization code
    pass
```

### Data Processing

Add custom data processing methods:

```python
def calculate_custom_metric(self, country_data):
    # Your custom calculation
    return custom_value
```

## Output Files

The application generates several output files:

- `covid_cases_map.png`: Total cases choropleth map
- `covid_deaths_map.png`: Total deaths choropleth map
- `covid_multiple_views.png`: Multiple metrics comparison
- `covid_time_series.png`: Time series plot
- `covid_data_export.csv`: Exported data for further analysis

## Error Handling

The application includes robust error handling:

- **Network Issues**: Falls back to sample data if online sources fail
- **Data Format Issues**: Handles missing or malformed data gracefully
- **Missing Dependencies**: Provides clear error messages for missing packages

## Performance Considerations

- **Data Caching**: Consider implementing data caching for large datasets
- **Memory Usage**: Monitor memory usage with large country datasets
- **Network Requests**: Implement rate limiting for API calls
- **Plot Rendering**: Use appropriate figure sizes for your use case

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Network Errors**: Check internet connection and try sample data
   ```python
   data = visualizer.fetch_covid_data('sample')
   ```

3. **Memory Issues**: Reduce dataset size or use smaller figure sizes

4. **Data Format Issues**: Check data source availability and format

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **Johns Hopkins University CSSE**: For providing comprehensive COVID-19 data
- **Our World in Data**: For additional data sources and analysis
- **Matplotlib Community**: For the excellent visualization library
- **Python Data Science Community**: For tools and best practices

## Support

For questions, issues, or contributions:

1. Check the documentation above
2. Review the code comments
3. Run the example usage script
4. Open an issue on the project repository

---

**Note**: This project uses publicly available data sources. Always verify data accuracy and follow proper attribution guidelines when using the visualizations.
