# ============================================================
# Flask Application - Nail Disease Diagnosis System
# ============================================================

# ---------------------------
# Importing Libraries
# ---------------------------
import os
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# ---------------------------
# Initialize Flask App
# ---------------------------
# Flask constructor takes the name of current module
app = Flask(__name__)

# ---------------------------
# Load the Trained Model
# ---------------------------
model = load_model('Vgg-16-nail-disease.h5')
print("Model loaded successfully!")

# ---------------------------
# Define Class Labels
# ---------------------------
# Must match alphabetical order of dataset/train/ folders
# (as assigned by flow_from_directory during training)
#
# Index -> Folder Name (sorted) -> Display Name
# 0  -> Darier_s disease     -> Darier's Disease
# 1  -> Muehrck-e_s lines    -> Muehrcke's Lines
# 2  -> aloperia areata      -> Alopecia Areata
# 3  -> beau_s lines         -> Beau's Lines
# 4  -> bluish nail          -> Bluish Nail
# 5  -> clubbing             -> Clubbing
# 6  -> eczema               -> Eczema
# 7  -> half and half nailes -> Half and Half Nails (Lindsay's Nails)
# 8  -> koilonychia          -> Koilonychia
# 9  -> leukonychia          -> Leukonychia
# 10 -> onycholycis          -> Onycholysis
# 11 -> pale nail            -> Pale Nail
# 12 -> red lunula           -> Red Lunula
# 13 -> splinter hemmorrage  -> Splinter Hemorrhage
# 14 -> terry_s nail         -> Terry's Nail
# 15 -> white nail           -> White Nail
# 16 -> yellow nails         -> Yellow Nails

class_labels = [
    "Darier's Disease",
    "Muehrcke's Lines",
    "Alopecia Areata",
    "Beau's Lines",
    "Bluish Nail",
    "Clubbing",
    "Eczema",
    "Half and Half Nails (Lindsay's Nails)",
    "Koilonychia",
    "Leukonychia",
    "Onycholysis",
    "Pale Nail",
    "Red Lunula",
    "Splinter Hemorrhage",
    "Terry's Nail",
    "White Nail",
    "Yellow Nails"
]

# Create uploads folder if it doesn't exist
os.makedirs('uploads', exist_ok=True)

# ---------------------------
# Route: Home Page (index.html)
# ---------------------------
@app.route('/')
def index():
    """Default home page"""
    return render_template('index.html')

# ---------------------------
# Route: About Page (about.html)
# ---------------------------
@app.route('/about')
def about():
    """When you click on about, redirects to about page"""
    return render_template('about.html')

# ---------------------------
# Route: Nail Disease Home Page (nailhome.html)
# ---------------------------
@app.route('/nailhome')
def nailhome():
    """When you click on nail, redirects to Nail Disease Home page"""
    return render_template('nailhome.html')

# ---------------------------
# Route: Nail Disease Prediction Page (nailpred.html)
# ---------------------------
@app.route('/nailpred')
def nailpred():
    """When you click on predict, redirects to Nail Predict page"""
    return render_template('nailpred.html')

# ---------------------------
# Route: Prediction (POST method)
# ---------------------------
@app.route('/predict', methods=['POST'])
def predict():
    """
    Requests the browsed file from HTML page using POST method.
    The picture file is saved to uploads folder.
    Image is loaded, preprocessed, and sent to model for prediction.
    Returns the class name to the predict variable in HTML page.
    """
    if request.method == 'POST':
        # Get the uploaded file from HTML page
        f = request.files['image']

        # Save to uploads folder using OS library
        file_path = os.path.join('uploads', f.filename)
        f.save(file_path)

        # Load image - VGG16 takes input format 224,224
        img = image.load_img(file_path, target_size=(224, 224))

        # Convert image to numpy array (image processing)
        img_array = image.img_to_array(img)

        # Normalize pixel values
        img_array = img_array / 255.0

        # Expand dimensions for model input
        img_array = np.expand_dims(img_array, axis=0)

        # Predict using the model
        preds = model.predict(img_array)

        # Get predicted class index (0th index)
        index = np.argmax(preds[0])

        # Get the class name using the index
        predicted_class = class_labels[index]

        # Render prediction to the predict variable in HTML page
        return render_template('nailpred.html', predict=predicted_class)

# ---------------------------
# Run the Application
# ---------------------------
# Runs on localhost:8080
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)