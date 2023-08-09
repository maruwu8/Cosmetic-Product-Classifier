import streamlit as st
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np

# Load the trained model
model = keras.models.load_model("classifier_model.h5")

# Define class labels
class_labels = ['bar-soap', 'blusher', 'body-butter-cream', 'concealer', 'eaux-de-parfum',
                'eyeliner', 'eyeshadow', 'face-powder', 'foundation', 'hairspray', 'lip-gloss',
                'lipstick', 'mascara', 'nail-varnish', 'shampoo']

# App description
description = (
    "Introducing the Cosmetic Product Classifier App! "
    "Ever been curious about the beauty products your significant other uses? "
    "This app has you covered. Just upload an image of a cosmetic item, and let modern technology reveal its "
    "category.\n\n No more guessing, only informed insights!.\n\n"
)

# Streamlit app
st.title("Cosmetic Product Classifier App 💄")
st.write(description)

# Upload image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    # Read image using PIL
    pil_image = Image.open(uploaded_image)

    # Display the uploaded image
    st.image(pil_image,
             caption="Uploaded Image",
             use_column_width=True)

    # Preprocess the image
    rgb_image = pil_image.convert('RGB')  # Convert to RGB (3 channels)
    resized_image = rgb_image.resize((224, 224))
    image_array = np.array(resized_image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # Predict class label
    predictions = model.predict(image_array)
    predicted_class_index = np.argmax(predictions)
    predicted_class_label = class_labels[predicted_class_index]
    confidence = predictions[0][predicted_class_index]

    # Display prediction
    st.subheader("Prediction:")
    st.write("Class:", predicted_class_label)
    st.write("Confidence:", confidence)
