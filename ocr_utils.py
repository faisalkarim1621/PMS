import requests
import base64

OCR_API_KEY = "K81994699488957"  # Replace with your actual API key

def process_image(image_file):
    url = "https://api.ocr.space/parse/image"

    # Convert image to base64
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

    payload = {
        "apikey": OCR_API_KEY,
        "base64image": f"data:image/png;base64,{image_data}",
        "language": "eng",
        "isOverlayRequired": False
    }

    response = requests.post(url, data=payload)
    result = response.json()

    if result.get("ParsedResults"):
        return result["ParsedResults"][0]["ParsedText"]
    return None
