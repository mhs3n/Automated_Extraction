from pdf2image import convert_from_path
import pytesseract
import os
from PIL import Image

# Path to the Tesseract executable (if not in PATH)
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"  # Adjust if necessary

# Convert PDF to images and apply preprocessing
def convert_pdf_to_images(pdf_path, output_folder="Data/output_images"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    

    pages = convert_from_path(pdf_path, 300)

    # Save each page as a preprocessed image
    image_paths = []
    for i, page in enumerate(pages):
        # Convert to grayscale (black & white)
        page = page.convert("L")  

        # Reduce size by half
        width, height = page.size
        page = page.resize((width // 2, height // 2))

        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        page.save(image_path, 'PNG')
        image_paths.append(image_path)

    return image_paths

# Perform OCR on each image
def ocr_from_images(image_paths, language='fra'):
    extracted_text = []
    
    for image_path in image_paths:
        text = pytesseract.image_to_string(image_path, lang=language)
        extracted_text.append(text)

    return "\n\n".join(extracted_text)

# Main function to process the PDF and extract text
def extract_text_from_pdf(pdf_path):
    # Step 1: Convert PDF to grayscale images
    image_paths = convert_pdf_to_images(pdf_path)

    # Step 2: Extract text using Tesseract OCR
    text = ocr_from_images(image_paths)

    # Save the output to a text file
    output_txt = pdf_path.replace('.pdf', '_output.txt')
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Text extracted and saved to {output_txt}")

# Example usage:
pdf_file_path = "/home/Ray/Desktop/Automated_extraction/Data/013Journal annonces2025.pdf"  # Replace with your PDF file path
extract_text_from_pdf(pdf_file_path)
