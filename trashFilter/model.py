import tensorflow as tf
import numpy as np
from mapping import mapping

model = tf.keras.applications.MobileNetV2(weights="imagenet")

def preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

def predict_trash(image_path):
    img = preprocess_image(image_path)
    preds = model.predict(img)
    decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0]
    label = decoded_preds[0][1]  


    for keyword, trash_bin in mapping.items():
        if keyword in label.lower():
            return f"{trash_bin} (détecté: {label})"

    return f"Poubelle Noire (détecté: {label})"
