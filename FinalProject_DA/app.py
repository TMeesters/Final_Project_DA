from flask import Flask, render_template, request, redirect, url_for, flash
import os 

import io
import re
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from google.cloud import vision
from nutrition_calculation import calculate_points_dynamically, calculate_nutrient_points, calculate_nutri_score
from utils import allowed_file, extract_text_from_image, parse_nutrition_facts


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = '4aa0a205891d712988ac69ac05994896'

UPLOAD_FOLDER = '/Users/jochemmeesters/Documents/Ironhack_DA/FinalProject_DA/uploaded_images'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
client = vision.ImageAnnotatorClient()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}


saved_products = []

@app.route('/')
def index():
    return render_template('main.html')


@app.route('/mylist')
def mylist():
    if saved_products:
        return render_template('mylist.html', products=saved_products)
    else:
        message = "Your saved products list is empty."
        return render_template('mylist.html', message=message)


@app.route('/nutriscore')
def nutriscore():
    return render_template('nutriscore.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with io.open(file_path, 'rb') as image_file: 
                content = image_file.read()

            extracted_text = extract_text_from_image(content)
            parsed_nutrition_facts = parse_nutrition_facts(extracted_text)
           
            if extracted_text:
            
                nutrition_facts = parse_nutrition_facts(extracted_text)
                nutri_score = calculate_nutri_score(nutrition_facts)
                print("Extracted Text:", extracted_text)
                print("Parsed Nutrition Facts:", nutrition_facts)
                
                
                if nutri_score:
                    flash('Image successfully uploaded', category='success')
                    return render_template('upload.html', extracted_text=extracted_text,
                                           nutrition_facts=nutrition_facts, nutri_score=nutri_score,
                                           image_path=file_path)
                else:
                    flash('Failed to calculate Nutri-score', category='error')
                    return render_template('upload.html', extracted_text=extracted_text)
            else:
                flash('No text found in the image.', category='error')
                return redirect(request.url)
        else:
            flash('File type not allowed', category='error')
            return redirect(request.url)

    return render_template('upload.html', extracted_text=None, nutrition_facts=None, nutri_score=None)




def handle_upload(image_content):
    extracted_text = extract_text_from_image(image_content)
    
    if extracted_text:
        # Check if there's enough information to calculate Nutri-score
        if all(key in extracted_text for key in ["Calories", "Total Fat", "Saturated Fat", "Sodium"]):
            # Parse nutrition facts
            nutrition_facts = parse_nutrition_facts(extracted_text)
            
            # Calculate total points
            total_points = calculate_total_points(nutrition_facts)
            
            # Calculate Nutri-score
            nutri_score = calculate_nutri_score(nutrition_facts)
            
            # Return the calculated values
            return {
                "extracted_text": extracted_text,
                "nutrition_facts": nutrition_facts,
                "total_points": total_points,
                "nutri_score": nutri_score
            }
        else:
            return {"error": "This label does not provide enough information of nutritional facts to calculate Nutri-score"}
    else:
        return {"error": "No text found in the image."}



@app.route('/save', methods=['POST'])
def save_product():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        nutri_score = request.form.get('nutri_score')
        if product_name and nutri_score:
            product = {'name': product_name, 'score': nutri_score}
            saved_products.append(product)
            flash('Product saved successfully!')
            return redirect(url_for('mylist'))
        else:
            flash('Missing product name or nutri score.')
    return redirect(url_for('upload'))


if __name__ == '__main__':
    app.run(debug=True)