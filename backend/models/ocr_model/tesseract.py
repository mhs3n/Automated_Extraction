from pdf2image import convert_from_path
import pytesseract
import os
import json
import numpy as np
import cv2

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"  # Adjust if needed

# Convert PDF to images with preprocessing
def convert_pdf_to_images(pdf_path):
    pages = convert_from_path(pdf_path, 300)  # Higher DPI for better OCR
    image_data = []

    for page in pages:
        # Convert the page to grayscale using PIL
        page = page.convert("L")

        # Convert the PIL image to a NumPy array for processing
        image = np.array(page)

        # Apply Gaussian Blur (removes small noise)
        image = cv2.GaussianBlur(image, (5, 5), 0)

        # Apply Adaptive Thresholding (binarization)
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)

        image_data.append(image)

    return image_data

# Split the image into columns (3 columns as per your requirement)
def split_image_into_columns(image, num_columns=3):
    height, width = image.shape[:2]
    column_width = width // num_columns  # Divide the width into 3 columns

    column_images = []
    for i in range(num_columns):
        # Extract each column
        column_image = image[:, i * column_width: (i + 1) * column_width]
        column_images.append(column_image)

    return column_images

# Perform OCR on each column
def ocr_from_columns(column_images, language='fra'):
    extracted_text = {}
    for i, column_image in enumerate(column_images):
        # Convert column to text using Tesseract OCR
        text = pytesseract.image_to_string(column_image, lang=language, config="--psm 6 --oem 1")
        extracted_text[f"column_{i+1}"] = text.strip()
    return extracted_text

# Perform OCR directly on the images, splitting into columns
def ocr_from_images(image_data, language='fra'):
    extracted_text = {}

    for i, image in enumerate(image_data):
        # Split the image into columns
        column_images = split_image_into_columns(image)

        # Perform OCR on each column
        column_text = ocr_from_columns(column_images, language)

        # Store text in dictionary for each page
        extracted_text[f"page_{i+1}"] = column_text

    return extracted_text

# Main function to process PDF and save as JSON
def extract_text_from_pdf(pdf_path):
    # Convert PDF to preprocessed images
    image_data = convert_pdf_to_images(pdf_path)

    # Extract text
    text_data = ocr_from_images(image_data)

    # Define output path and save JSON file
    output_json = pdf_path.replace('.pdf', '_output.json').replace('/kaggle/input/', '/kaggle/working/text/')
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(text_data, f, ensure_ascii=False, indent=4)

    print(f"Text extracted and saved to {output_json}")

# Example usage
pdf_file_path = "Data/013Journal annonces2025.pdf"  # Update the path for your local machine
extract_text_from_pdf(pdf_file_path)
