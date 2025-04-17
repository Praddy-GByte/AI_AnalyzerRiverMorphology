import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import tempfile
import shutil
from folium.plugins import Draw, MeasureControl, Fullscreen, MousePosition
import json

# Load environment variables
load_dotenv()

# Deployment configuration
st.set_page_config(
    page_title="River Morphology AI Analyzer",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache configuration for better performance
@st.cache_data
def load_data():
    # Add your data loading logic here
    return None

# ASU Theme Colors
ASU_COLORS = {
    'maroon': '#8C1D40',
    'gold': '#FFC627',
    'light_gold': '#FFD100',
    'dark_maroon': '#5C0025',
    'light_maroon': '#A73E5C'
}

# Custom CSS with Professional Design
st.markdown(f"""
    <style>
    /* Base Styles */
    .main {{
        padding: 2rem;
        background-color: #f8f9fa;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .main {{
            padding: 1rem;
        }}
        .metric-card {{
            margin-bottom: 1rem;
        }}
        .header-section h1 {{
            font-size: 1.8rem !important;
        }}
    }}
    
    /* Side Borders */
    .stApp {{
        border-left: 8px solid {ASU_COLORS['gold']};
        border-right: 8px solid {ASU_COLORS['maroon']};
    }}
    
    /* Enhanced Components */
    .stButton>button {{
        width: 100%;
        background-color: white;
        color: {ASU_COLORS['maroon']};
        border: 2px solid {ASU_COLORS['maroon']};
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }}
    .stButton>button:hover {{
        background-color: {ASU_COLORS['maroon']};
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    .metric-card {{
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: all 0.3s ease;
        border-left: 4px solid {ASU_COLORS['gold']};
        border-right: 4px solid {ASU_COLORS['maroon']};
    }}
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }}
    
    .header-section {{
        background-color: white;
        padding: 3rem;
        border-radius: 15px;
        color: {ASU_COLORS['maroon']};
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        border: 2px solid {ASU_COLORS['maroon']};
    }}
    .header-section::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: {ASU_COLORS['gold']};
    }}
    
    .sidebar-section {{
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid {ASU_COLORS['gold']};
    }}
    
    .info-tile {{
        background-color: white;
        color: {ASU_COLORS['maroon']};
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid {ASU_COLORS['maroon']};
        position: relative;
        overflow: hidden;
        height: auto;
    }}
    
    .info-tile h3 {{
        font-weight: 600;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
        font-size: 1rem;
    }}
    
    .info-tile p {{
        line-height: 1.4;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 0;
    }}
    
    /* Location Info Styles */
    .location-info {{
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid {ASU_COLORS['maroon']};
    }}
    
    .location-info h3 {{
        color: {ASU_COLORS['maroon']};
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }}
    
    .location-detail {{
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }}
    
    .location-detail:last-child {{
        border-bottom: none;
    }}
    
    .location-label {{
        color: #666;
        font-weight: 500;
    }}
    
    .location-value {{
        color: {ASU_COLORS['maroon']};
        font-weight: 600;
    }}
    
    .map-container {{
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid {ASU_COLORS['gold']};
    }}
    
    .tab-content {{
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid {ASU_COLORS['gold']};
    }}
    
    .footer {{
        background-color: white;
        color: {ASU_COLORS['maroon']};
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        position: relative;
        border: 2px solid {ASU_COLORS['maroon']};
    }}
    .footer::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: {ASU_COLORS['gold']};
    }}
    
    .stSelectbox, .stSlider, .stRadio {{
        border-left: 3px solid {ASU_COLORS['gold']};
        padding-left: 10px;
    }}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: #f1f1f1;
    }}
    ::-webkit-scrollbar-thumb {{
        background: {ASU_COLORS['maroon']};
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {ASU_COLORS['dark_maroon']};
    }}
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        padding: 1rem 2rem;
        border-radius: 10px;
        transition: all 0.3s ease;
        color: {ASU_COLORS['maroon']};
        font-weight: 500;
        letter-spacing: 0.5px;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {ASU_COLORS['light_maroon']};
        color: white;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {ASU_COLORS['maroon']};
        color: white;
    }}
    
    /* Info Tile Icons */
    .info-icon {{
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: {ASU_COLORS['maroon']};
        opacity: 0.8;
    }}
    
    /* Professional Typography */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Arial', sans-serif;
        letter-spacing: 0.5px;
    }}
    
    .header-section h1 {{
        font-weight: 700;
        letter-spacing: 1px;
    }}
    
    .info-tile h3 {{
        font-weight: 600;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }}
    
    .info-tile p {{
        line-height: 1.6;
        color: #666;
    }}
    
    /* Feature Tags */
    .feature-tag {{
        display: inline-block;
        padding: 0.5rem 1rem;
        border: 1px solid {ASU_COLORS['maroon']};
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }}
    .feature-tag:hover {{
        background-color: {ASU_COLORS['maroon']};
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

# Header section with professional design
st.markdown("""
    <div class="header-section">
        <h1 style="margin-bottom: 0.5rem; font-size: 2.5rem;">River Morphology AI Analyzer</h1>
        <p style="opacity: 0.9; font-size: 1.2rem; line-height: 1.6;">Advanced satellite-based river channel analysis and prediction system</p>
        <div style="display: flex; gap: 1rem; margin-top: 1.5rem; flex-wrap: wrap;">
            <span class="feature-tag">Global Coverage</span>
            <span class="feature-tag">AI-Powered Analysis</span>
            <span class="feature-tag">Real-time Monitoring</span>
            <span class="feature-tag">Multi-Sensor Data</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Info tiles with professional design
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="info-tile">
            <h3>Global Coverage</h3>
            <p>Comprehensive river network analysis with high-resolution satellite imagery</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="info-tile">
            <h3>Advanced Analytics</h3>
            <p>State-of-the-art machine learning for precise morphology prediction</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="info-tile">
            <h3>Comprehensive Features</h3>
            <p>Multi-faceted analysis including channel detection and erosion assessment</p>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="info-tile">
            <h3>Responsive Design</h3>
            <p>Optimized interface for all devices and screen sizes</p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar for user inputs with enhanced organization
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    
    # Data Source Selection with enhanced options
    st.subheader("Data Source")
    data_source = st.radio(
        "Select data source",
        ["Upload Shapefile", "Draw on Map", "Select Predefined", "Import from GEE"],
        key="data_source"
    )
    
    if data_source == "Upload Shapefile":
        uploaded_file = st.file_uploader("Upload River Shapefile", type=['shp', 'dbf', 'shx', 'prj'])
        if uploaded_file:
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            try:
                gdf = gpd.read_file(file_path)
                st.success("Shapefile uploaded successfully!")
            except Exception as e:
                st.error(f"Error reading shapefile: {str(e)}")
            finally:
                shutil.rmtree(temp_dir)
    
    # Date range selection with enhanced options
    st.subheader("Time Period")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=365),
            key="start_date"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now(),
            key="end_date"
        )
    
    # Base Layer Selection with enhanced options
    st.subheader("Base Layer")
    base_layer = st.selectbox(
        "Select base layer",
        ["OpenStreetMap", "Stamen Terrain", "Satellite", "Topographic", "Sentinel-2", "Landsat-8", "SRTM"],
        key="base_layer"
    )
    
    # Analysis type with enhanced options
    st.subheader("Analysis Type")
    analysis_type = st.multiselect(
        "Select analyses to perform",
        ["Channel Detection", "Erosion Analysis", "Meander Migration", "Future Prediction", 
         "Sediment Transport", "Flood Risk", "Water Quality", "Habitat Assessment"],
        key="analysis_type"
    )
    
    # Advanced parameters with enhanced options
    st.subheader("Advanced Parameters")
    col1, col2 = st.columns(2)
    with col1:
        resolution = st.slider("Analysis Resolution (m)", 10, 100, 30)
    with col2:
        confidence = st.slider("Confidence Threshold (%)", 70, 100, 90)
    
    # Display Options with enhanced features
    st.subheader("Display Options")
    col1, col2 = st.columns(2)
    with col1:
        show_contours = st.checkbox("Show Contours", value=True)
        show_heatmap = st.checkbox("Show Heatmap", value=True)
    with col2:
        show_annotations = st.checkbox("Show Annotations", value=True)
        show_3d = st.checkbox("Show 3D View", value=False)
    
    # Export Options
    st.subheader("Export Options")
    export_format = st.selectbox(
        "Select export format",
        ["GeoJSON", "Shapefile", "CSV", "PDF Report"],
        key="export_format"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area with enhanced tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Map View", "Time Series", "Analysis Results", "3D View", "Reports"])

with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.header("Interactive Map")
    
    # Initialize map with selected base layer
    base_layers = {
        "OpenStreetMap": "OpenStreetMap",
        "Stamen Terrain": "Stamen Terrain",
        "Satellite": "Esri.WorldImagery",
        "Topographic": "Esri.WorldTopoMap",
        "Sentinel-2": "https://tiles.maps.eox.at/wms?service=wms&request=getcapabilities",
        "Landsat-8": "https://tiles.maps.eox.at/wms?service=wms&request=getcapabilities",
        "SRTM": "https://tiles.maps.eox.at/wms?service=wms&request=getcapabilities"
    }
    
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles=base_layers[base_layer])
    
    # Add enhanced drawing tools
    draw = Draw(
        draw_options={
            'polyline': True,
            'polygon': True,
            'circle': True,
            'rectangle': True,
            'marker': True,
            'circlemarker': True
        }
    )
    draw.add_to(m)
    
    # Add enhanced controls
    measure = MeasureControl(
        position='topright',
        primary_length_unit='meters',
        secondary_length_unit='kilometers',
        primary_area_unit='sqmeters',
        secondary_area_unit='sqkilometers'
    )
    measure.add_to(m)
    
    # Add mouse position
    MousePosition().add_to(m)
    
    # Add fullscreen control
    Fullscreen().add_to(m)
    
    # Add a sample river polygon with enhanced styling
    folium.GeoJson(
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [78.0, 20.5],
                    [78.5, 20.6],
                    [79.0, 20.4],
                    [79.5, 20.7]
                ]
            },
            "properties": {
                "name": "Sample River"
            }
        },
        style_function=lambda x: {
            'color': ASU_COLORS['maroon'],
            'weight': 3,
            'opacity': 0.7,
            'dashArray': '5, 5'
        }
    ).add_to(m)
    
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    folium_static(m)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.header("Time Series Analysis")
    if not analysis_type:
        st.info("Please select analysis type(s) from the sidebar to view time series data.")
    else:
        # Generate enhanced time series data
        dates = pd.date_range(start=start_date, end=end_date, periods=20)
        data = pd.DataFrame({
            'Channel Width': np.random.normal(100, 10, 20),
            'Migration Rate': np.random.normal(15, 2, 20),
            'Erosion': np.random.normal(2.5, 0.5, 20),
            'Sediment Load': np.random.normal(1200, 100, 20),
            'Water Depth': np.random.normal(5, 1, 20)
        }, index=dates)
        
        # Create enhanced time series plot
        fig = go.Figure()
        for column in data.columns:
            fig.add_trace(go.Scatter(
                x=dates,
                y=data[column],
                name=column,
                line=dict(width=3),
                mode='lines+markers',
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="River Morphology Metrics Over Time",
            xaxis_title="Date",
            yaxis_title="Metric Value",
            template='plotly_white',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.header("Analysis Results")
    if not analysis_type:
        st.info("Please select analysis type(s) from the sidebar to view results.")
    else:
        # Enhanced metric cards with more information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.subheader("Channel Statistics")
            st.metric("Average Width Change", "2.5 m", "+0.3 m")
            st.metric("Migration Rate", "15 m/year", "-2 m/year")
            st.metric("Channel Length", "45.2 km", "+1.2 km")
            st.metric("Channel Slope", "0.002", "-0.0001")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.subheader("Erosion Analysis")
            st.metric("Erosion Area", "2.3 km²", "+0.5 km²")
            st.metric("Deposition Area", "1.8 km²", "-0.2 km²")
            st.metric("Erosion Rate", "1.2 m/year", "+0.1 m/year")
            st.metric("Sediment Yield", "1500 t/km²/year", "+200 t/km²/year")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional metrics with enhanced visualization
        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.subheader("Water Quality")
            st.metric("Turbidity", "15 NTU", "-2 NTU")
            st.metric("Sediment Load", "1200 t/day", "+150 t/day")
            st.metric("Dissolved Oxygen", "8.2 mg/L", "+0.3 mg/L")
            st.metric("pH Level", "7.4", "-0.1")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.subheader("Environmental Impact")
            st.metric("Vegetation Loss", "0.8 km²", "+0.2 km²")
            st.metric("Habitat Change", "1.5 km²", "-0.3 km²")
            st.metric("Biodiversity Index", "0.75", "-0.05")
            st.metric("Carbon Storage", "1200 tC", "-50 tC")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced visualizations
        st.subheader("Advanced Visualizations")
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            # Erosion heatmap with enhanced styling
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.subheader("Erosion Heatmap")
            heatmap_data = np.random.rand(10, 10)
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data,
                colorscale='Reds',
                showscale=True,
                hoverongaps=False
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with viz_col2:
            # Channel profile with enhanced styling
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.subheader("Channel Profile")
            profile_data = np.random.rand(20)
            fig = go.Figure(data=go.Scatter(
                y=profile_data,
                mode='lines',
                line=dict(color=ASU_COLORS['maroon'], width=3),
                fill='tozeroy',
                fillcolor=f'rgba(140, 29, 64, 0.2)'
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                showlegend=False,
                yaxis=dict(title='Elevation (m)'),
                xaxis=dict(title='Distance (m)')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.header("3D View")
    st.info("3D visualization coming soon!")
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.header("Reports")
    st.info("Report generation coming soon!")
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
    <div class="footer">
        <div style="text-align: center;">
            <h3 style="font-weight: 600; letter-spacing: 1px;">Powered by Advanced Technologies</h3>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem; flex-wrap: wrap;">
                <span style="font-weight: 500;">Google Earth Engine</span>
                <span style="font-weight: 500;">TensorFlow</span>
                <span style="font-weight: 500;">Streamlit</span>
                <span style="font-weight: 500;">Sentinel-2</span>
                <span style="font-weight: 500;">Landsat-8</span>
            </div>
            <p style="margin-top: 1.5rem; color: #666;">© 2024 River Morphology AI Analyzer | Research and Environmental Monitoring</p>
        </div>
    </div>
    """, unsafe_allow_html=True) 