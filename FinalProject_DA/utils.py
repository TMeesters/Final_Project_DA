import re
import os 
from google.cloud import vision

UPLOAD_FOLDER = '/Users/jochemmeesters/Documents/Ironhack_DA/FinalProject_DA/uploaded_images'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
client = vision.ImageAnnotatorClient()

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_image(image_data):
    try:
        # Initialize Google Cloud Vision client
        client = vision.ImageAnnotatorClient()

        # Convert image data to Google Cloud Vision image format
        image = vision.Image(content=image_data)

        # Perform text detection on the image
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            return texts[0].description
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None


def parse_nutrition_facts(extracted_text):
    nutrition_facts = {}
    parsing_rules = {
        'Total Fat': r'Total\s*Fat.*?(\d+(?:\.\d+)?)\s*(\w+)',
        'Sodium': r'Sodium.*?(\d+(?:\.\d+)?)\s*(\w+)',
        'Total Carbohydrate': r'Total\s*Carbohydrate.*?(\d+(?:\.\d+)?)\s*(\w+)',
        'Sugars': r'Sugars.*?(\d+(?:\.\d+)?)\s*(\w+)',
        'Protein': r'Protein.*?(\d+(?:\.\d+)?)\s*(\w+)',
        'Calcium': r'Calcium.*?(\d+(?:\.\d+)?)\s*(\w+)',
        'Iron': r'Iron.*?(\d+(?:\.\d+)?)\s*(\w+)',
    }
    
    for nutrient, pattern in parsing_rules.items():
        match = re.search(pattern, extracted_text, re.IGNORECASE)
        if match:
            value = match.group(1)
            unit = match.group(2)
            nutrition_facts[nutrient] = {'value': value, 'unit': unit}
        else:
            nutrition_facts[nutrient] = {'value': None, 'unit': None}
    
    return nutrition_facts

def display_nutrition_info(nutrition_facts):
    print("Nutrition Facts:")
    for nutrient, data in nutrition_facts.items():
        if data:
            value = data.get('value')
            unit = data.get('unit')
            if value is not None:
                try:
                    value = float(value)
                    if value == 0:
                        print(f"{nutrient}: None")
                    elif value < 1:
                        print(f"{nutrient}: Less than 1 {unit}")
                    else:
                        print(f"{nutrient}: {value} {unit}")
                except ValueError:
                    print(f"{nutrient}: None")
            else:
                print(f"{nutrient}: None")
        else:
            print(f"{nutrient}: None")

