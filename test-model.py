# ============================================================
# Test the Model
# ============================================================

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# ---------------------------
# Load the Saved Model
# ---------------------------
model = load_model('Vgg-16-nail-disease.h5')
print("Model loaded successfully!")

# ---------------------------
# Define Class Labels
# ---------------------------
# IMPORTANT: These MUST match the alphabetical order of
# training folders as assigned by flow_from_directory
#
# Python sorts uppercase before lowercase (ASCII order):
#   D(68) < M(77) < a(97) < b(98) < c(99) < e(101) ...
#
# Folder Name (sorted)              -> Index
# ----------------------------------------
# Darier_s disease                   -> 0
# Muehrck-e_s lines                  -> 1
# aloperia areata                    -> 2
# beau_s lines                       -> 3
# bluish nail                        -> 4
# clubbing                           -> 5
# eczema                             -> 6
# half and half nailes (Lindsay_s nails) -> 7
# koilonychia                        -> 8
# leukonychia                        -> 9
# onycholycis                        -> 10
# pale nail                          -> 11
# red lunula                         -> 12
# splinter hemmorrage                -> 13
# terry_s nail                       -> 14
# white nail                         -> 15
# yellow nails                       -> 16

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

# ---------------------------
# Take an Image as Input
# ---------------------------
# Change this path to any image from your test folder
test_image_path = 'dataset/test/bluish nail/1.PNG'

# VGG16 requires 224x224 input
img = image.load_img(test_image_path, target_size=(224, 224))

# Convert to numpy array
img_array = image.img_to_array(img)

# Normalize pixel values
img_array = img_array / 255.0

# Expand dimensions: (224,224,3) -> (1,224,224,3)
img_array = np.expand_dims(img_array, axis=0)

print(f"Image shape: {img_array.shape}")

# ---------------------------
# Predict Using the Model
# ---------------------------
predictions = model.predict(img_array)

# Get predicted class index
predicted_class_index = np.argmax(predictions[0])

# Get predicted class name
predicted_class_name = class_labels[predicted_class_index]

# Print the predicted class
print(f"\nPredicted Class Index: {predicted_class_index}")
print(f"Predicted Class Name: {predicted_class_name}")
print(f"Confidence: {predictions[0][predicted_class_index] * 100:.2f}%")

# Print all probabilities
print(f"\nAll Class Probabilities:")
for i, (label, prob) in enumerate(zip(class_labels, predictions[0])):
    print(f"  {i}: {label} - {prob * 100:.2f}%")