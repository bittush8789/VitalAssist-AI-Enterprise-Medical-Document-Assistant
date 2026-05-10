import cv2
import numpy as np
from PIL import Image

def preprocess_image(image_path):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Denoising
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    
    # Thresholding
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Sharpening
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(thresh, -1, kernel)
    
    # Skew correction (Simplified)
    # In a real enterprise app, we'd do more robust skew detection
    
    preprocessed_path = image_path.replace(".", "_preprocessed.")
    cv2.imwrite(preprocessed_path, sharpened)
    
    return preprocessed_path
