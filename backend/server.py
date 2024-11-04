from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from extractor import extract_text_from_image, extract_data
from PIL import Image
import re
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the frontend

# Set the path for Tesseract (if needed)
# pytesseract.pytesseract.tesseract_cmd = '/path/to/tesseract'

def extract_text_from_image(image_path):
    # Use pytesseract to extract text from the image
    return pytesseract.image_to_string(Image.open(image_path))

def extract_data(text):
    # Define regex patterns for name, document number, and expiration date
    name_pattern = r"(?i)(?:Name|Holder|Licensee):?\s*([A-Za-z\s]+)"
    doc_number_pattern = r"(?i)(?:DL|Document Number|ID Number):?\s*([A-Z0-9]+)"
    expiration_date_pattern = r"(?i)(?:Expires|Expiration Date|EXP):?\s*(\d{1,2}/\d{1,2}/\d{2,4})"

    # Search for matches in the text
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

@app.route('/extract', methods=['POST'])
def extract():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Extract text from the image
    extracted_text = extract_text_from_image(file_path)

    # Extract relevant data
    extracted_data = extract_data(extracted_text)

    # Clean up by deleting the file after processing
    os.remove(file_path)

    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True)
