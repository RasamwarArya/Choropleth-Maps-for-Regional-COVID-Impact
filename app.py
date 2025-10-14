"""
Flask Web Application for COVID-19 Data Visualization
Serves choropleth maps and interactive visualizations
"""

from flask import Flask, render_template, jsonify, send_file
import os
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg
from covid_choropleth import COVIDChoroplethMap
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web serving

app = Flask(__name__)

# Global visualizer instance
visualizer = None

def get_visualizer():
    """Get or create the COVID visualizer instance"""
    global visualizer
    if visualizer is None:
        visualizer = COVIDChoroplethMap()
        visualizer.covid_data = visualizer.fetch_covid_data('jhu')
        visualizer.world_data = visualizer.load_world_data()
    return visualizer

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string for web display"""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return image_base64

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/statistics')
def get_statistics():
    """Get global COVID-19 statistics"""
    viz = get_visualizer()
    
    total_cases = sum(data.get('cases', 0) for data in viz.covid_data.values())
    total_deaths = sum(data.get('deaths', 0) for data in viz.covid_data.values())
    total_recovered = sum(data.get('recovered', 0) for data in viz.covid_data.values())
    total_active = sum(data.get('active', 0) for data in viz.covid_data.values())
    
    # Top 10 countries by cases
    country_cases = [(country, data['cases']) for country, data in viz.covid_data.items()]
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
    """Generate choropleth map for specific data type"""
    viz = get_visualizer()
    
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
    
    fig, ax = viz.create_choropleth_map(data_type, color_schemes[data_type], (12, 8))
    image_base64 = fig_to_base64(fig)
    
    return jsonify({'image': image_base64})

@app.route('/api/multiple_views')
def get_multiple_views():
    """Generate multiple views dashboard"""
    viz = get_visualizer()
    
    fig, axes = viz.create_multiple_views((16, 12))
    image_base64 = fig_to_base64(fig)
    
    return jsonify({'image': image_base64})

@app.route('/api/time_series')
def get_time_series():
    """Generate time series plot"""
    viz = get_visualizer()
    
    fig, ax = viz.create_time_series_plot()
    image_base64 = fig_to_base64(fig)
    
    return jsonify({'image': image_base64})

@app.route('/api/static/<filename>')
def static_files(filename):
    """Serve static files (images)"""
    static_dir = os.path.join(app.root_path, 'static')
    file_path = os.path.join(static_dir, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return jsonify({'error': 'File not found'}), 404

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
