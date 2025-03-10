import json
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import base64

# Function to process album data
def process_album_data(album_data):
    """
    Process the album data for visualizations.
    
    Args:
        album_data (list): List of dictionaries containing album information
    
    Returns:
        pandas.DataFrame: Processed dataframe of album data
    """
    # Convert to DataFrame
    df = pd.DataFrame(album_data)
    
    # Convert chart positions, replacing '-' with NaN
    df['US_peak_chart_post'] = pd.to_numeric(df['US_peak_chart_post'], errors='coerce')
    
    return df

# Create Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('Sales Performance Dashboard', 
            style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'marginBottom': '20px'
        },
        multiple=False
    ),
    
    html.Div(id='error-message', style={'color': 'red', 'marginBottom': '20px'}),
    
    html.Div([
        # Line Chart
        html.Div([
            html.H2('Chart Performance Over Time'),
            dcc.Graph(id='line-chart')
        ], className='chart-container'),
        
        # Bar Chart
        html.Div([
            html.H2('Album Release Frequency'),
            dcc.Graph(id='bar-chart')
        ], className='chart-container'),
        
        # Scatter Plot
        html.Div([
            html.H2('Year vs Chart Position'),
            dcc.Graph(id='scatter-chart')
        ], className='chart-container'),
        
        # Heatmap
        html.Div([
            html.H2('Year vs Chart Performance'),
            dcc.Graph(id='heatmap-chart')
        ], className='chart-container'),
        
        # Treemap
        html.Div([
            html.H2('Album Performance Distribution'),
            dcc.Graph(id='treemap-chart')
        ], className='chart-container')
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'})
])

# Callback to handle file upload and generate charts
@app.callback(
    [Output('line-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('scatter-chart', 'figure'),
     Output('heatmap-chart', 'figure'),
     Output('treemap-chart', 'figure'),
     Output('error-message', 'children')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_dashboard(contents, filename):
    if not contents:
        return [go.Figure() for _ in range(5)] + ['Please upload a JSON file']
    
    try:
        # Decode and parse JSON
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string).decode('utf-8')
        album_data = json.loads(decoded)
        
        # Process data
        df = process_album_data(album_data)
        
        # Filter out non-charting albums
        charting_df = df[df['US_peak_chart_post'].notna()]
        
        # 1. Line Chart: Chart Performance Over Time
        line_fig = go.Figure(data=go.Scatter(
            x=charting_df['album'], 
            y=charting_df['US_peak_chart_post'],
            mode='lines+markers',
            name='Chart Position'
        ))
        line_fig.update_layout(
            title='Chart Performance Over Time',
            yaxis_title='Chart Position',
            yaxis_autorange='reversed'
        )
        
        # 2. Bar Chart: Album Release Frequency
        release_freq = df['year'].value_counts().sort_index()
        bar_fig = go.Figure(data=go.Bar(
            x=release_freq.index, 
            y=release_freq.values,
            marker_color='green'
        ))
        bar_fig.update_layout(
            title='Album Release Frequency',
            xaxis_title='Year',
            yaxis_title='Number of Albums'
        )
        
        # 3. Scatter Plot: Year vs Chart Position
        scatter_fig = go.Figure(data=go.Scatter(
            x=charting_df['year'], 
            y=charting_df['US_peak_chart_post'],
            text=charting_df['album'],
            mode='markers',
            marker=dict(
                size=10,
                color=charting_df['US_peak_chart_post'],
                colorscale='Viridis'
            )
        ))
        scatter_fig.update_layout(
            title='Year vs Chart Position',
            xaxis_title='Year',
            yaxis_title='Chart Position',
            yaxis_autorange='reversed'
        )
        
        # 4. Heatmap: Year vs Chart Performance
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=charting_df['US_peak_chart_post'].values.reshape(-1, 1),
            x=charting_df['year'],
            y=['Chart Position'],
            colorscale='Viridis'
        ))
        heatmap_fig.update_layout(title='Year vs Chart Performance')
        
        # 5. Treemap: Album Performance Distribution
        def get_performance_tier(position):
            if pd.isna(position):
                return 'No Chart'
            elif position <= 5:
                return 'Top 5'
            elif position <= 10:
                return 'Top 10'
            elif position <= 50:
                return 'Top 50'
            else:
                return 'No Chart'
        
        df['performance_tier'] = df['US_peak_chart_post'].apply(get_performance_tier)
        tier_counts = df['performance_tier'].value_counts()
        
        treemap_fig = go.Figure(go.Treemap(
            labels=tier_counts.index,
            parents=[''] * len(tier_counts),
            values=tier_counts.values,
            texttemplate='%{label}<br>%{value} Albums'
        ))
        treemap_fig.update_layout(title='Album Performance Distribution')
        
        return [line_fig, bar_fig, scatter_fig, heatmap_fig, treemap_fig, '']
    
    except Exception as e:
        return [go.Figure() for _ in range(5)] + [f'Error processing file: {str(e)}']

# Additional CSS for styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .chart-container {
                width: 45%;
                margin-bottom: 20px;
            }
            @media (max-width: 768px) {
                .chart-container {
                    width: 100%;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)