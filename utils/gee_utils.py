import ee
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def get_sentinel2_collection(start_date, end_date, region):
    """
    Get Sentinel-2 imagery collection for the specified date range and region
    """
    # Filter Sentinel-2 collection
    collection = (ee.ImageCollection('COPERNICUS/S2_SR')
        .filterDate(start_date, end_date)
        .filterBounds(region)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    )
    return collection

def get_landsat_collection(start_date, end_date, region):
    """
    Get Landsat 8/9 imagery collection for the specified date range and region
    """
    # Filter Landsat collection
    collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
        .filterDate(start_date, end_date)
        .filterBounds(region)
        .filter(ee.Filter.lt('CLOUD_COVER', 20))
    )
    return collection

def calculate_ndwi(image):
    """
    Calculate Normalized Difference Water Index (NDWI)
    """
    ndwi = image.normalizedDifference(['B3', 'B8'])
    return ndwi

def calculate_ndvi(image):
    """
    Calculate Normalized Difference Vegetation Index (NDVI)
    """
    ndvi = image.normalizedDifference(['B8', 'B4'])
    return ndvi

def get_time_series(collection, region, band='B4'):
    """
    Extract time series data for a specific band and region
    """
    def extract_values(image):
        stats = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=30
        )
        return ee.Feature(None, {
            'date': image.date().format('YYYY-MM-dd'),
            'value': stats.get(band)
        })
    
    time_series = collection.map(extract_values)
    return time_series

def export_to_geojson(feature_collection, filename):
    """
    Export feature collection to GeoJSON
    """
    task = ee.batch.Export.table.toDrive(
        collection=feature_collection,
        description=filename,
        fileFormat='GeoJSON'
    )
    task.start()
    return task

def get_river_mask(image, threshold=0.2):
    """
    Create binary mask for river channels using NDWI
    """
    ndwi = calculate_ndwi(image)
    river_mask = ndwi.gt(threshold)
    return river_mask

def calculate_channel_width(river_mask, scale=30):
    """
    Calculate river channel width from binary mask
    """
    # Convert to vector
    vectors = river_mask.reduceToVectors(
        geometry=river_mask.geometry(),
        scale=scale,
        geometryType='polygon',
        eightConnected=False,
        labelProperty='label'
    )
    
    # Calculate width statistics
    def calculate_stats(feature):
        width = feature.geometry().perimeter().divide(2)
        return feature.set('width', width)
    
    stats = vectors.map(calculate_stats)
    return stats 