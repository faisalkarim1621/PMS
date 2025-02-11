import pytesseract
from PIL import Image
import io

def process_image(file_storage):
    """
    Process an uploaded image file using Tesseract OCR
    """
    try:
        # Reset file pointer to beginning
        file_storage.seek(0)

        # Read image data
        image_data = file_storage.read()

        # Create image from binary data
        image_stream = io.BytesIO(image_data)
        image = Image.open(image_stream)

        # Convert image to text using Tesseract
        text = pytesseract.image_to_string(image)

        # Reset file pointer for potential future reads
        file_storage.seek(0)

        return text.strip()
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")