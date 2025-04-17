import folium
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

def create_folium_map(center_lat=20, center_lon=78, zoom_start=5):
    """
    Create a base Folium map
    """
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap'
    )
    return m

def add_river_layer(map_obj, river_mask, name='River Channel'):
    """
    Add river channel layer to Folium map
    """
    # Convert binary mask to GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Add river channel as a polygon
    contours, _ = cv2.findContours(
        river_mask.astype(np.uint8),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    for contour in contours:
        if len(contour) > 2:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [contour.squeeze().tolist()]
                }
            }
            geojson["features"].append(feature)
    
    # Add layer to map
    folium.GeoJson(
        geojson,
        name=name,
        style_function=lambda x: {
            'fillColor': '#3388ff',
            'color': '#3388ff',
            'weight': 2,
            'fillOpacity': 0.5
        }
    ).add_to(map_obj)
    
    return map_obj

def plot_time_series(data, title='River Morphology Time Series'):
    """
    Create interactive time series plot
    """
    fig = go.Figure()
    
    # Add traces for each metric
    for column in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[column],
                name=column,
                mode='lines+markers'
            )
        )
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Value',
        hovermode='x unified',
        showlegend=True
    )
    
    return fig

def plot_morphological_metrics(metrics):
    """
    Create bar plot of morphological metrics
    """
    fig = go.Figure()
    
    for metric_name, values in metrics.items():
        fig.add_trace(
            go.Box(
                y=values,
                name=metric_name,
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8
            )
        )
    
    fig.update_layout(
        title='Morphological Metrics Distribution',
        yaxis_title='Value',
        showlegend=False
    )
    
    return fig

def plot_erosion_deposition(erosion_area, deposition_area):
    """
    Create pie chart of erosion and deposition areas
    """
    fig = go.Figure(data=[go.Pie(
        labels=['Erosion', 'Deposition'],
        values=[erosion_area, deposition_area],
        hole=.3
    )])
    
    fig.update_layout(
        title='Erosion vs Deposition Areas',
        annotations=[dict(text='Area', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    return fig 