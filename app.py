"""
Flask Web Application for COVID-19 Data Visualization (Optimized for Render)
Serves simple charts and interactive visualizations
"""

from flask import Flask, render_template, jsonify, send_file
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web serving
import matplotlib.pyplot as plt
plt.ioff()  # Turn off interactive mode
import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Global data cache
covid_data = None

def get_covid_data():
    """Get COVID-19 data - use sample data for speed"""
    global covid_data
    if covid_data is None:
        # Generate sample data for demonstration
        countries = [
            'United States of America', 'China', 'India', 'Brazil', 'Russia',
            'United Kingdom', 'France', 'Germany', 'Italy', 'Spain',
            'Canada', 'Australia', 'Japan', 'South Korea', 'Mexico',
            'Argentina', 'Chile', 'Colombia', 'Peru', 'South Africa'
        ]
        
        covid_data = {}
        for country in countries:
            cases = np.random.randint(100000, 10000000)
            deaths = int(cases * np.random.uniform(0.01, 0.05))
            recovered = int(cases * np.random.uniform(0.7, 0.9))
            active = cases - deaths - recovered
            
            covid_data[country] = {
                'cases': cases,
                'deaths': deaths,
                'recovered': recovered,
                'active': max(0, active)
            }
    
    return covid_data

def create_simple_chart(data_type, color_scheme, figsize=(12, 6)):
    """Create a simple bar chart for web deployment"""
    try:
        data = get_covid_data()
        
        # Get data for top countries
        country_data = []
        for country, country_info in data.items():
            if data_type in country_info and country_info[data_type] > 0:
                country_data.append((country, country_info[data_type]))
        
        # Sort by value and take top 15 countries
        country_data.sort(key=lambda x: x[1], reverse=True)
        top_countries = country_data[:15]
        
        if not top_countries:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, f'No data available for {data_type}', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            ax.set_title(f'COVID-19 {data_type.replace("_", " ").title()} - Top Countries', 
                        fontsize=14, fontweight='bold')
            return fig, ax
        
        # Create bar chart
        countries = [country[:12] + '...' if len(country) > 12 else country for country, _ in top_countries]
        values = [value for _, value in top_countries]
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Color schemes
        color_schemes = {
            'Reds': plt.cm.Reds,
            'Blues': plt.cm.Blues,
            'Greens': plt.cm.Greens,
            'Oranges': plt.cm.Oranges
        }
        
        cmap = color_schemes.get(color_scheme, plt.cm.Reds)
        colors = cmap(np.linspace(0.3, 1.0, len(countries)))
        
        bars = ax.bar(range(len(countries)), values, color=colors)
        
        ax.set_title(f'COVID-19 {data_type.replace("_", " ").title()} - Top Countries', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Countries', fontsize=10)
        ax.set_ylabel(f'{data_type.replace("_", " ").title()}', fontsize=10)
        
        # Set x-axis labels
        ax.set_xticks(range(len(countries)))
        ax.set_xticklabels(countries, rotation=45, ha='right', fontsize=8)
        
        # Format y-axis
        if max(values) > 1000000:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        elif max(values) > 1000:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.1f}K'))
        
        plt.tight_layout()
        return fig, ax
        
    except Exception as e:
        print(f"Error creating simple chart: {e}")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, f'Error loading {data_type} data', 
               ha='center', va='center', transform=ax.transAxes, fontsize=14)
        ax.set_title(f'COVID-19 {data_type.replace("_", " ").title()}', 
                    fontsize=14, fontweight='bold')
        return fig, ax

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string for web display"""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close(fig)  # Close figure to free memory
    return image_base64

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/statistics')
def get_statistics():
    """Get global COVID-19 statistics"""
    data = get_covid_data()
    
    total_cases = sum(country_data.get('cases', 0) for country_data in data.values())
    total_deaths = sum(country_data.get('deaths', 0) for country_data in data.values())
    total_recovered = sum(country_data.get('recovered', 0) for country_data in data.values())
    total_active = sum(country_data.get('active', 0) for country_data in data.values())
    
    # Top 10 countries by cases
    country_cases = [(country, country_data['cases']) for country, country_data in data.items()]
    country_cases.sort(key=lambda x: x[1], reverse=True)
    top_countries = country_cases[:10]
    
    stats = {
        'total_cases': total_cases,
        'total_deaths': total_deaths,
        'total_recovered': total_recovered,
        'total_active': total_active,
        'death_rate': (total_deaths/total_cases*100) if total_cases > 0 else 0,
        'recovery_rate': (total_recovered/total_cases*100) if total_cases > 0 else 0,
        'top_countries': [{'country': country, 'cases': cases} for country, cases in top_countries]
    }
    
    return jsonify(stats)

@app.route('/api/map/<data_type>')
def get_map(data_type):
    """Generate chart for specific data type"""
    try:
        # Valid data types
        valid_types = ['cases', 'deaths', 'recovered', 'active']
        if data_type not in valid_types:
            return jsonify({'error': 'Invalid data type'}), 400
        
        # Color schemes for different data types
        color_schemes = {
            'cases': 'Reds',
            'deaths': 'Reds', 
            'recovered': 'Greens',
            'active': 'Oranges'
        }
        
        # Create a simple bar chart
        fig, ax = create_simple_chart(data_type, color_schemes[data_type])
        image_base64 = fig_to_base64(fig)
        
        return jsonify({'image': image_base64})
    except Exception as e:
        return jsonify({'error': f'Failed to generate chart: {str(e)}'}), 500

@app.route('/api/multiple_views')
def get_multiple_views():
    """Generate multiple views dashboard"""
    try:
        data_types = ['cases', 'deaths', 'recovered', 'active']
        color_schemes = ['Reds', 'Blues', 'Greens', 'Oranges']
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        axes = axes.flatten()
        
        for i, (data_type, color_scheme) in enumerate(zip(data_types, color_schemes)):
            ax = axes[i]
            
            # Get data for this type
            data = get_covid_data()
            country_data = []
            for country, country_info in data.items():
                if data_type in country_info and country_info[data_type] > 0:
                    country_data.append((country, country_info[data_type]))
            
            country_data.sort(key=lambda x: x[1], reverse=True)
            top_countries = country_data[:10]
            
            if top_countries:
                countries = [country[:10] + '...' if len(country) > 10 else country for country, _ in top_countries]
                values = [value for _, value in top_countries]
                
                cmap = getattr(plt.cm, color_scheme)
                colors = cmap(np.linspace(0.3, 1.0, len(countries)))
                
                ax.bar(range(len(countries)), values, color=colors)
                ax.set_title(f'{data_type.replace("_", " ").title()}', fontsize=12, fontweight='bold')
                ax.set_xticks(range(len(countries)))
                ax.set_xticklabels(countries, rotation=45, ha='right', fontsize=8)
                
                if max(values) > 1000000:
                    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
                elif max(values) > 1000:
                    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.1f}K'))
            else:
                ax.text(0.5, 0.5, f'No data for {data_type}', ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f'{data_type.replace("_", " ").title()}', fontsize=12, fontweight='bold')
        
        plt.suptitle('COVID-19 Multiple Views Dashboard', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        image_base64 = fig_to_base64(fig)
        return jsonify({'image': image_base64})
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate multiple views: {str(e)}'}), 500

@app.route('/api/time_series')
def get_time_series():
    """Generate time series plot"""
    try:
        data = get_covid_data()
        
        # Top 10 countries by cases
        country_cases = [(country, country_data['cases']) for country, country_data in data.items()]
        country_cases.sort(key=lambda x: x[1], reverse=True)
        top_countries = country_cases[:10]
        
        countries = [country[:15] + '...' if len(country) > 15 else country for country, _ in top_countries]
        values = [value for _, value in top_countries]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        bars = ax.bar(range(len(countries)), values, color=plt.cm.viridis(np.linspace(0, 1, len(countries))))
        
        ax.set_title('COVID-19 Cases by Country', fontsize=16, fontweight='bold')
        ax.set_xlabel('Country', fontsize=12)
        ax.set_ylabel('Total Cases', fontsize=12)
        ax.set_xticks(range(len(countries)))
        ax.set_xticklabels(countries, rotation=45, ha='right')
        
        # Format y-axis
        if max(values) > 1000000:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        elif max(values) > 1000:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.1f}K'))
        
        plt.tight_layout()
        
        image_base64 = fig_to_base64(fig)
        return jsonify({'image': image_base64})
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate time series: {str(e)}'}), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
