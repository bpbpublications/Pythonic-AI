# -*- coding: utf-8 -*-
"""Ch9.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NqHm7q9e7JR_Ro5W1y_lh0-YTaliKM98
"""

import numpy as np
import tensorflow as tf

batch_size = 32
timesteps = 10
input_dim = 20

x = np.random.random((batch_size, timesteps, input_dim))
print("Shape of the data: ", x.shape)

input_shape = (timesteps, input_dim) 
inputs = tf.keras.Input(shape=input_shape, batch_size=batch_size)

rnn_layer = tf.keras.layers.SimpleRNN(units=64)(inputs)
dense_layer = tf.keras.layers.Dense(units=32)(rnn_layer)
model = tf.keras.models.Model(inputs=inputs, outputs=dense_layer)

model.summary()

model= tf.keras.models.Sequential([
    tf.keras.layers.Embedding(100,64, name='embedding'),
    tf.keras.layers.SimpleRNN(64, return_sequences=True),
    tf.keras.layers.SimpleRNN(64),
    tf.keras.layers.Dense(1, activation='sigmoid')])

model.summary()

import numpy as np
import tensorflow as tf

batch_size = 32
timesteps = 10
input_dim = 20

x = np.random.random((batch_size, timesteps, input_dim))

input_shape = (timesteps, input_dim) 
inputs = tf.keras.Input(shape=input_shape, batch_size=batch_size)
rnn_layer = tf.keras.layers.RNN(tf.keras.layers.SimpleRNNCell(units=64))(inputs)
dense_layer = tf.keras.layers.Dense(units=32)(rnn_layer)
model = tf.keras.models.Model(inputs=inputs, outputs=dense_layer)

model.summary()

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Embedding(100,64))
model.add(tf.keras.layers.LSTM(64, return_sequences=True))
model.add(tf.keras.layers.LSTM(64))
model.add(tf.keras.layers.Dense(units=1))

model.summary()

input_shape = (timesteps, input_dim) 
inputs = tf.keras.Input(shape=input_shape, batch_size=batch_size)
lstm_layer = tf.keras.layers.RNN(tf.keras.layers.LSTMCell(units=64))(inputs)
dense_layer = tf.keras.layers.Dense(units=32)(lstm_layer)
model = tf.keras.models.Model(inputs=inputs, outputs=dense_layer)

model.summary()

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Embedding(100,64))
model.add(tf.keras.layers.GRU(64, return_sequences=True))
model.add(tf.keras.layers.GRU(64))
model.add(tf.keras.layers.Dense(units=1))

model.summary()

input_shape = (timesteps, input_dim) 
inputs = tf.keras.Input(shape=input_shape, batch_size=batch_size)
gru_layer = tf.keras.layers.RNN(tf.keras.layers.GRUCell(units=64))(inputs)
dense_layer = tf.keras.layers.Dense(units=32)(gru_layer)
model = tf.keras.models.Model(inputs=inputs, outputs=dense_layer)

model.summary()

input_shape = (timesteps, input_dim) 
inputs = tf.keras.Input(shape=input_shape, batch_size=batch_size)

bidirectional_layer = tf.keras.layers.Bidirectional(
    layer=tf.keras.layers.GRU(units=64, return_sequences=True), 
    backward_layer=tf.keras.layers.LSTM(units=64, return_sequences=True, go_backwards=True))(inputs)

dense_layer = tf.keras.layers.Dense(units=1)(bidirectional_layer)
model = tf.keras.models.Model(inputs=inputs, outputs=dense_layer)

model.summary()

import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding

# Prepare training data
text = "The quick brown fox jumps over the lazy dog"
words = text.lower().split()
unique_words = sorted(set(words))
word_to_index = dict((word, index) for index, word in enumerate(unique_words))
index_to_word = dict((index, word) for index, word in enumerate(unique_words))
X_train = []
y_train = []
for i in range(len(words) - 1):
    X_train.append(word_to_index[words[i]])
    y_train.append(word_to_index[words[i + 1]])
X_train = np.array(X_train)
y_train = np.array(y_train)

# Define LSTM model architecture
model = Sequential()
model.add(Embedding(len(unique_words), 50, input_length=1))
model.add(LSTM(100))
model.add(Dense(len(unique_words), activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, validation_split=0.2, epochs=500, verbose=2)

# Predict the next word
seed_text = "quick"

# Convert seed text to integer indexed sequence
sequence = [word_to_index[word] for word in seed_text.split()]
# Pad sequence to fixed length
sequence = np.reshape(sequence, (len(sequence), 1))
# Predict the next word in the sequence
prediction = model.predict(sequence, verbose=0)
# Convert prediction to word
print(prediction)
print(np.argmax(prediction))
next_word = index_to_word[np.argmax(prediction)]
# Append next word to seed text
seed_text += " " + next_word
print(seed_text)

LENGTH_WORD = 5
next_words = []
prev_words = []
for j in range(len(words) - LENGTH_WORD):
     prev_words.append(words[j:j + LENGTH_WORD])
     next_words.append(words[j + LENGTH_WORD])
print(prev_words[0])
print(next_words[0])

unique_words = np.unique(words)
unique_word_index = dict((c, i) for i, c in enumerate(unique_words))

X = np.zeros((len(prev_words), LENGTH_WORD, len(unique_words)), dtype=bool)
Y = np.zeros((len(next_words), len(unique_words)), dtype=bool)
for i, each_words in enumerate(prev_words):
   for j, each_word in enumerate(each_words):
        X[i, j, unique_word_index[each_word]] = 1
   Y[i, unique_word_index[next_words[i]]] = 1

X.shape

!python -m spacy download en_core_web_sm
#!wget "http://nlp.stanford.edu/data/glove.6B.zip"
#!unzip glove.6B.zip

import pathlib
import spacy
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

nlp = spacy.load('en_core_web_sm')
input_file = "book.txt"
doc = nlp(pathlib.Path(input_file).read_text(encoding="utf-8"))

words = []
for token in doc:
    if token.is_alpha:
        words.append(token.text.lower())
unique_words = np.unique(words)

clean_text = " ".join(words)

SEQ_LENGTH = 30
char_sequences = list()

for j in range(len(clean_text) - SEQ_LENGTH):
    char_sequences.append(clean_text[j:j + SEQ_LENGTH + 1])

len(char_sequences)

char_sequences[:5]

unique_chars = sorted(list(set(clean_text)))
char_to_idx = dict((c, i) for i, c in enumerate(unique_chars))
idx_to_char = dict((i, c) for i, c in enumerate(unique_chars))

encoded_sequence = list()
for seq in char_sequences:
    encoded_sequence.append([char_to_idx[char] for char in seq])

vocab_len = len(char_to_idx)
encoded_sequence = np.array(encoded_sequence)

X, y = encoded_sequence[:,:-1], encoded_sequence[:,-1]

#y = tf.keras.utils.to_categorical(y, num_classes=vocab)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

print('Train shape:', X_train.shape, 'Val shape:', X_test.shape)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Embedding(vocab_len, 50, input_length=30, trainable=True))
model.add(tf.keras.layers.GRU(100, dropout=0.6))
model.add(tf.keras.layers.Dense(vocab, activation='softmax'))
model.summary()

model.compile(loss='sparse_categorical_crossentropy', metrics=['sparse_categorical_accuracy'], optimizer='adam')
model.fit(X_train, y_train, epochs=20, verbose=2, validation_data=(X_test, y_test))

def generate_sequence(model, char_to_idx, idx_to_char, input_seq, num_chars):
    for i in range(num_chars):
        encoded = [char_to_idx[char] for char in input_seq]
        encoded = tf.keras.utils.pad_sequences([encoded], maxlen=30)
        pred = model.predict(encoded, verbose=0)
        gen_char = idx_to_char[np.argmax(pred[0])]
        input_seq = input_seq + gen_char
        
    return input_seq

generate_sequence(model, idx_to_char, "the group closely observed the s", 10)

generate_sequence(model, idx_to_char, "they closely observed that it", 10)

generate_sequence(model, idx_to_char, "the king appeared in front of me", 15)

len("the king appeared in front of me")

import tensorflow as tf
import numpy as np
sequences = [[1, 7], [9, 2, ], [3, 6, 8, 4]]
tf.keras.utils.pad_sequences(sequences, padding="post", value=-999)
