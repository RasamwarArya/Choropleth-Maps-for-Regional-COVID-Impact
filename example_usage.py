"""
Example usage of the COVID-19 Choropleth Map Visualization
This script demonstrates various ways to use the COVIDChoroplethMap class
"""

from covid_choropleth import COVIDChoroplethMap
import matplotlib.pyplot as plt

def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    # Create visualizer instance
    visualizer = COVIDChoroplethMap()
    
    # Fetch data from Johns Hopkins University
    print("Fetching data from JHU...")
    visualizer.covid_data = visualizer.fetch_covid_data('jhu')
    
    # Create a simple cases map
    fig, ax = visualizer.create_choropleth_map('cases', 'Reds', (12, 8))
    plt.title('COVID-19 Total Cases by Country')
    plt.show()

def example_multiple_data_sources():
    """Example using different data sources"""
    print("\n=== Multiple Data Sources Example ===")
    
    visualizer = COVIDChoroplethMap()
    
    # Try different data sources
    sources = ['jhu', 'owid', 'sample']
    
    for source in sources:
        print(f"\nFetching data from {source.upper()}...")
        data = visualizer.fetch_covid_data(source)
        
        if data:
            print(f"Successfully loaded data for {len(data)} countries")
            # Create a map for each source
            fig, ax = visualizer.create_choropleth_map('cases', 'Blues', (10, 6))
            plt.title(f'COVID-19 Cases - {source.upper()} Data Source')
            plt.show()

def example_different_metrics():
    """Example showing different COVID-19 metrics"""
    print("\n=== Different Metrics Example ===")
    
    visualizer = COVIDChoroplethMap()
    visualizer.covid_data = visualizer.fetch_covid_data('jhu')
    
    # Different metrics to visualize
    metrics = [
        ('cases', 'Reds', 'Total Cases'),
        ('deaths', 'Reds', 'Total Deaths'),
        ('recovered', 'Greens', 'Total Recovered'),
        ('active', 'Oranges', 'Active Cases')
    ]
    
    for metric, color_scheme, title in metrics:
        print(f"Creating map for {title}...")
        fig, ax = visualizer.create_choropleth_map(metric, color_scheme, (12, 8))
        plt.title(f'COVID-19 {title} by Country')
        plt.show()

def example_custom_analysis():
    """Example of custom analysis and visualization"""
    print("\n=== Custom Analysis Example ===")
    
    visualizer = COVIDChoroplethMap()
    visualizer.covid_data = visualizer.fetch_covid_data('jhu')
    
    # Print detailed statistics
    visualizer.print_statistics()
    
    # Create multiple views
    print("\nCreating multiple views...")
    fig, axes = visualizer.create_multiple_views((20, 15))
    plt.suptitle('COVID-19 Global Impact - Comprehensive View')
    plt.show()
    
    # Create time series for top countries
    print("\nCreating time series plot...")
    fig, ax = visualizer.create_time_series_plot()
    plt.title('Top 10 Countries by COVID-19 Cases')
    plt.show()

def example_specific_countries():
    """Example focusing on specific countries"""
    print("\n=== Specific Countries Example ===")
    
    visualizer = COVIDChoroplethMap()
    visualizer.covid_data = visualizer.fetch_covid_data('jhu')
    
    # Focus on specific countries
    target_countries = [
        'United States of America', 'China', 'India', 'Brazil', 'Russia',
        'United Kingdom', 'France', 'Germany', 'Italy', 'Spain'
    ]
    
    print("Analyzing specific countries...")
    for country in target_countries:
        if country in visualizer.covid_data:
            data = visualizer.covid_data[country]
            print(f"\n{country}:")
            print(f"  Cases: {data['cases']:,}")
            print(f"  Deaths: {data['deaths']:,}")
            print(f"  Recovered: {data['recovered']:,}")
            print(f"  Active: {data['active']:,}")
            if data['population'] > 0:
                print(f"  Cases per Million: {data['cases_per_million']:.1f}")
                print(f"  Deaths per Million: {data['deaths_per_million']:.1f}")

def example_data_export():
    """Example of exporting data for further analysis"""
    print("\n=== Data Export Example ===")
    
    visualizer = COVIDChoroplethMap()
    visualizer.covid_data = visualizer.fetch_covid_data('jhu')
    
    # Convert to DataFrame for analysis
    import pandas as pd
    
    data_list = []
    for country, data in visualizer.covid_data.items():
        data_list.append({
            'Country': country,
            'Cases': data['cases'],
            'Deaths': data['deaths'],
            'Recovered': data['recovered'],
            'Active': data['active'],
            'Population': data['population'],
            'Cases_Per_Million': data.get('cases_per_million', 0),
            'Deaths_Per_Million': data.get('deaths_per_million', 0)
        })
    
    df = pd.DataFrame(data_list)
    
    # Save to CSV
    df.to_csv('covid_data_export.csv', index=False)
    print("Data exported to 'covid_data_export.csv'")
    
    # Display summary statistics
    print("\nData Summary:")
    print(df.describe())
    
    # Top 10 countries by cases
    print("\nTop 10 Countries by Cases:")
    top_countries = df.nlargest(10, 'Cases')[['Country', 'Cases', 'Deaths']]
    print(top_countries.to_string(index=False))

def example_error_handling():
    """Example of error handling and fallback options"""
    print("\n=== Error Handling Example ===")
    
    visualizer = COVIDChoroplethMap()
    
    # Try to fetch data with error handling
    try:
        print("Attempting to fetch data from JHU...")
        data = visualizer.fetch_covid_data('jhu')
        if data:
            print("JHU data loaded successfully")
        else:
            print("JHU data failed, trying OWID...")
            data = visualizer.fetch_covid_data('owid')
            if data:
                print("OWID data loaded successfully")
            else:
                print("All online sources failed, using sample data")
                data = visualizer.fetch_covid_data('sample')
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Using sample data as fallback")
        data = visualizer.fetch_covid_data('sample')
    
    # Create visualization regardless of data source
    fig, ax = visualizer.create_choropleth_map('cases', 'Reds', (12, 8))
    plt.title('COVID-19 Cases - Data Source: ' + ('JHU' if 'jhu' in str(type(data)) else 'Sample'))
    plt.show()

if __name__ == "__main__":
    print("COVID-19 Choropleth Map - Example Usage")
    print("="*50)
    
    # Run all examples
    try:
        example_basic_usage()
        example_multiple_data_sources()
        example_different_metrics()
        example_custom_analysis()
        example_specific_countries()
        example_data_export()
        example_error_handling()
        
        print("\n" + "="*50)
        print("All examples completed successfully!")
        print("Check the generated files and plots.")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Please check your internet connection and try again.")
