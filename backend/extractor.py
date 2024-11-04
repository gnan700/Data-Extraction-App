import pytesseract
from PIL import Image
import re

def extract_text_from_image(image_path):
    """
    Extracts text from the given image using Tesseract OCR.
    
    Parameters:
        image_path (str): Path to the image file.
        
    Returns:
        str: The text extracted from the image.
    """
    return pytesseract.image_to_string(Image.open(image_path))

def extract_data(text):
    """
    Extracts name, document number, and expiration date from the given text using regular expressions.
    
    Parameters:
        text (str): Text extracted from the image.
        
    Returns:
        dict: A dictionary with the extracted name, document number, and expiration date.
    """
    # Define regex patterns
    name_pattern = r"(?i)(?:Name|Holder|Licensee):?\s*([A-Za-z\s]+)"
    doc_number_pattern = r"(?i)(?:DL|Document Number|ID Number):?\s*([A-Z0-9]+)"
    expiration_date_pattern = r"(?i)(?:Expires|Expiration Date|EXP):?\s*(\d{1,2}/\d{1,2}/\d{2,4})"

    # Search for matches
    name_match = re.search(name_pattern, text)
    doc_number_match = re.search(doc_number_pattern, text)
    expiration_date_match = re.search(expiration_date_pattern, text)

    # Prepare extracted data dictionary
    extracted_data = {
        "name": name_match.group(1).strip() if name_match else None,
        "document_number": doc_number_match.group(1).strip() if doc_number_match else None,
        "expiration_date": expiration_date_match.group(1).strip() if expiration_date_match else None,
    }
    return extracted_data
