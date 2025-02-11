import pytesseract
from PIL import Image
import io

def process_image(file_storage):
    """
    Process an uploaded image file using Tesseract OCR
    """
    try:
        # Read image from file storage
        image_stream = io.BytesIO(file_storage.read())
        image = Image.open(image_stream)
        
        # Convert image to text using Tesseract
        text = pytesseract.image_to_string(image)
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")
