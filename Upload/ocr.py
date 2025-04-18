import easyocr
import json
import re
import numpy as np
import cv2

# def to_grayscale(image):
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# def binarize_image(image):
#     grayscale = to_grayscale(image)
#     _, binary_image = cv2.threshold(grayscale, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     return binary_image

# def apply_gaussian_blur(image):
#     return cv2.GaussianBlur(image, (5, 5), 0)

# def dilate_image(image):
#     kernel = np.ones((2, 2), np.uint8)
#     return cv2.dilate(image, kernel, iterations=1)

# def erode_image(image):
#     kernel = np.ones((2, 2), np.uint8)
#     return cv2.erode(image, kernel, iterations=1)

# def enhance_contrast(image):
#     grayscale = to_grayscale(image)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     return clahe.apply(grayscale)

# def resize_image(image, scale_percent=150):
#     width = int(image.shape[1] * scale_percent / 100)
#     height = int(image.shape[0] * scale_percent / 100)
#     return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

# def deskew_image(image):
#     grayscale = to_grayscale(image)
#     coords = np.column_stack(np.where(grayscale > 0))
#     angle = cv2.minAreaRect(coords)[-1]
#     if angle < -45:
#         angle = -(90 + angle)
#     else:
#         angle = -angle
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# def remove_noise(image):
#     return cv2.medianBlur(image, 5)

# def recognize_text(img_path):
#     # Preprocess the image
#     preprocessed_image = preprocess_image(img_path)

#     # Save preprocessed image temporarily (optional)
#     cv2.imwrite('preprocessed_image.png', preprocessed_image)

#     # Read text using OCR from preprocessed image
#     reader = easyocr.Reader(['en'])
#     result = reader.readtext(preprocessed_image)
#     return result

# def preprocess_image(img_path):
#     image = cv2.imread(img_path)

#     # Apply preprocessing steps
#     image = to_grayscale(image)
#     image = enhance_contrast(image)
#     image = binarize_image(image)
#     image = apply_gaussian_blur(image)
#     image = dilate_image(image)
#     image = deskew_image(image)
#     image = resize_image(image)
    
#     return image

def recognize_text(img_path):
    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path)

def extract_information(result):
    # Print the raw OCR result for reference
    print("OCR Result:", result)

    # Filter high-confidence results (confidence > 0.10)
    filtered_data = [entry for entry in result if entry[2] > 0.10]
    text_strings = [entry[1] for entry in filtered_data]

    # Print the filtered results
    print("Filtered OCR Result:", text_strings)

    name = None
    dob = None
    id_number = None
    gender = None

    # Define regex patterns for DOB, gender, and Aadhaar number (12 digits)
    dob_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')  # Date pattern (DD/MM/YYYY)
    id_pattern = re.compile(r'\d{4}\s\d{4}\s\d{4}')  # Aadhaar number pattern
    gender_pattern = re.compile(r'\b(male|female)\b', re.IGNORECASE)  # Gender pattern

    for text in text_strings:
        text = text.strip()

        # Check for gender (male/female)
        gender_match = gender_pattern.search(text)
        if gender_match and not gender:
            gender = gender_match.group().capitalize()

        # Check for DOB using the regex pattern
        dob_match = dob_pattern.search(text)
        if dob_match and not dob:
            dob = dob_match.group()

        # Check for Aadhaar number (12 digits)
        id_match = id_pattern.search(text)
        if id_match and not id_number:
            id_number = id_match.group().replace(' ', '')

        # Heuristic to find name - we assume the name is typically a non-numeric string without 'DOB', 'Male', 'Female'
        if not any(keyword in text.lower() for keyword in ['dob', 'male', 'female']) and not re.search(r'\d', text):
            # Assuming name appears in uppercase or title case format (heuristic)
            if name is None or len(name.split()) < 2:  # Prefer names with 2 words or more
                name = text

    # Create JSON object with the extracted info
    info = {
        'id': id_number if id_number else 'Not found',
        'name': name if name else 'Not found',
        'DOB': dob if dob else 'Not found',
        'gender': gender if gender else 'Not found',
    }

    return info

def process_image(img_path):
    result = recognize_text(img_path)
    information = extract_information(result)
    return json.dumps(information, indent=4)
