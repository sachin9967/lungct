import cv2
import numpy as np

IMG_SIZE = 224

def preprocess_image(image_path):
    """
    Preprocess image for CNN embedding model.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        np.ndarray: Preprocessed image ready for model input
    """
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Invalid image")

    img = cv2.resize(
        img,
        (IMG_SIZE, IMG_SIZE)
    )

    img = img.astype(np.float32)

    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    return img
