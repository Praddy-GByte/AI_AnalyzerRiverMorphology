import numpy as np
import cv2
from skimage import measure
from scipy import ndimage

def preprocess_image(image, target_size=(256, 256)):
    """
    Preprocess image for model input
    """
    # Resize image
    image = cv2.resize(image, target_size)
    
    # Normalize pixel values
    image = image.astype(np.float32) / 255.0
    
    return image

def postprocess_mask(mask, threshold=0.5):
    """
    Postprocess model output mask
    """
    # Apply threshold
    binary_mask = (mask > threshold).astype(np.uint8)
    
    # Remove small objects
    binary_mask = remove_small_objects(binary_mask, min_size=100)
    
    # Fill holes
    binary_mask = ndimage.binary_fill_holes(binary_mask)
    
    return binary_mask

def remove_small_objects(mask, min_size=100):
    """
    Remove small objects from binary mask
    """
    # Label connected components
    labeled_mask = measure.label(mask)
    
    # Get properties of each region
    props = measure.regionprops(labeled_mask)
    
    # Create new mask without small objects
    new_mask = np.zeros_like(mask)
    for prop in props:
        if prop.area >= min_size:
            new_mask[labeled_mask == prop.label] = 1
    
    return new_mask

def calculate_morphological_metrics(mask):
    """
    Calculate morphological metrics from binary mask
    """
    # Label connected components
    labeled_mask = measure.label(mask)
    props = measure.regionprops(labeled_mask)
    
    metrics = {
        'area': [],
        'perimeter': [],
        'eccentricity': [],
        'solidity': []
    }
    
    for prop in props:
        metrics['area'].append(prop.area)
        metrics['perimeter'].append(prop.perimeter)
        metrics['eccentricity'].append(prop.eccentricity)
        metrics['solidity'].append(prop.solidity)
    
    return metrics

def detect_meander_shifts(mask1, mask2):
    """
    Detect meander shifts between two masks
    """
    # Calculate distance transform
    dist1 = cv2.distanceTransform(mask1, cv2.DIST_L2, 5)
    dist2 = cv2.distanceTransform(mask2, cv2.DIST_L2, 5)
    
    # Calculate difference
    diff = np.abs(dist1 - dist2)
    
    # Threshold to get significant changes
    significant_changes = diff > 5
    
    return significant_changes

def calculate_erosion_deposition(mask1, mask2):
    """
    Calculate erosion and deposition areas
    """
    # Erosion (areas in mask1 but not in mask2)
    erosion = np.logical_and(mask1, np.logical_not(mask2))
    
    # Deposition (areas in mask2 but not in mask1)
    deposition = np.logical_and(mask2, np.logical_not(mask1))
    
    # Calculate areas
    erosion_area = np.sum(erosion)
    deposition_area = np.sum(deposition)
    
    return erosion_area, deposition_area 