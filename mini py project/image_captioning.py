import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.models import Model # type: ignore
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, add
import numpy as np
import pickle
import os

def load_image(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

# Extract features using a pre-trained CNN
def extract_features(img_path, model):
    img = load_image(img_path)
    features = model.predict(img, verbose=0)
    return features

# Load caption data
def load_doc(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

def create_tokenizer(captions_list):
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(captions_list)
    return tokenizer

def max_length(captions_list):
    return max(len(caption.split()) for caption in captions_list)

# Define the caption generator model
def define_model(vocab_size, max_length):
    inputs1 = tf.keras.layers.Input(shape=(2048,))
    fe1 = Dense(256, activation='relu')(inputs1)
    fe2 = tf.keras.layers.RepeatVector(max_length)(fe1)

    inputs2 = tf.keras.layers.Input(shape=(max_length,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = LSTM(256, return_sequences=True)(se1)
    se3 = tf.keras.layers.TimeDistributed(Dense(256))(se2)

    decoder1 = add([fe2, se3])
    decoder2 = LSTM(256)(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

# Generate captions for images
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = word_for_id(yhat, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text

if __name__ == "__main__":
    # Load the pre-trained InceptionV3 model
    model = InceptionV3(weights='imagenet')
    model_new = Model(model.input, model.layers[-2].output)

    # Load your captions file
    filename = 'captions.txt'
    doc = load_doc(filename)
    captions_list = doc.split('\n')
    tokenizer = create_tokenizer(captions_list)
    vocab_size = len(tokenizer.word_index) + 1
    max_length = max_length(captions_list)

    # Define the caption generation model
    model = define_model(vocab_size, max_length)
    model.summary()

    # Load the pre-trained weights
    model.load_weights('model_weights.h5')

    # Generate caption for a new image
    img_path = 'example.jpg'
    photo = extract_features(img_path, model_new)
    description = generate_desc(model, tokenizer, photo, max_length)
    print(description)
