# ============================================================
# Model Building - VGG16 Nail Disease Diagnosis
# ============================================================

# ---------------------------
# Importing the Libraries
# ---------------------------
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ---------------------------
# Loading the Model
# ---------------------------
# VGG16 with ImageNet weights, excluding top classification layers
# Input shape: 224x224x3 (VGG16 requirement)
IMAGE_SIZE = [224, 224]
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# ---------------------------
# Adding Flatten Layers
# ---------------------------
# Freeze all hidden layers (keep pre-trained weights)
# Hidden layers freeze because they have trained sequence
for layer in vgg.layers:
    layer.trainable = False

# ---------------------------
# Adding Output Layer
# ---------------------------
# Flatten the VGG16 output
x = Flatten()(vgg.output)

# 17 indicates number of classes
# softmax is the activation function for categorical output
prediction = Dense(17, activation='softmax')(x)

# ---------------------------
# Creating a Model Object
# ---------------------------
# Creating inputs and outputs and fitting to VGG16 model
model = Model(inputs=vgg.input, outputs=prediction)

# View model architecture
model.summary()

# ---------------------------
# Configure the Learning Process
# ---------------------------
# Loss function: categorical_crossentropy (for multi-class)
# Optimizer: Adam
# Metrics: accuracy
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# ---------------------------
# Import ImageDataGenerator Library
# ---------------------------
# Configure ImageDataGenerator class
# Data augmentation techniques:
# - rescale: normalize pixel values to [0,1]
# - shear_range: shear transformation
# - zoom_range: random zoom
# - horizontal_flip: randomly flip images
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

# ---------------------------
# Apply ImageDataGenerator to Trainset and Testset
# ---------------------------
# flow_from_directory returns batches of images from subdirectories
# Arguments:
#   directory: path to data
#   target_size: resize images to 224x224
#   batch_size: 10
#   class_mode: 'categorical' for multi-class classification

training_set = train_datagen.flow_from_directory(
    'dataset/train',
    target_size=(224, 224),
    batch_size=10,
    class_mode='categorical'
)

test_set = test_datagen.flow_from_directory(
    'dataset/test',
    target_size=(224, 224),
    batch_size=10,
    class_mode='categorical'
)

# Print class indices to verify label order
print("\nClass Indices (folder -> index mapping):")
print(training_set.class_indices)
print(f"\nTotal training images: {training_set.samples}")
print(f"Total test images: {test_set.samples}")
print(f"Number of classes: {len(training_set.class_indices)}")

# ---------------------------
# Train the Model
# ---------------------------
# fit (replaces deprecated fit_generator)
# steps_per_epoch = total training samples / batch_size
# validation_steps = total test samples / batch_size
# epochs = 30 (can increase for better accuracy)

r = model.fit(
    training_set,
    validation_data=test_set,
    epochs=30,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
)

# ---------------------------
# Save the Model
# ---------------------------
# Save with .h5 extension (Hierarchical Data Format)
model.save('Vgg-16-nail-disease.h5')
print("\nModel saved as 'Vgg-16-nail-disease.h5'")