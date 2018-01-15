import tensorflow as tf

import keras
import numpy as np
from keras.layers import Input, LSTM, RepeatVector, Dense, Embedding, Activation, Masking, SimpleRNN
from keras.layers.wrappers import TimeDistributed
from keras.models import Model, Sequential
from keras import backend as K
from keras.callbacks import ModelCheckpoint

import sys


import json

VOC_SIZE = 3503
mask_val = 0
out_dim = 100
LSTM_INTERNAL_DIM = 500

#ENCODER 
encoder_input = Input(shape=(None,))

encoder_embedding_layer = Embedding(VOC_SIZE + 1, out_dim, mask_zero=True)
encoder_embedding = encoder_embedding_layer(encoder_input)

encoder_recurent_layer_1 = LSTM(LSTM_INTERNAL_DIM, return_state=True, return_sequences=True )
encoder_recurent_1, encoder_h, encoder_c = encoder_recurent_layer_1(encoder_embedding)

#encoder_recurent_layer_2 = LSTM(LSTM_INTERNAL_DIM, return_state=True, return_sequences=True )
#encoder_recurent_2, encoder_h_2, encoder_c_2 = encoder_recurent_layer_2(encoder_recurent_1)

encoder_out_layer = TimeDistributed(Dense(VOC_SIZE, activation='softmax'))
encoder_out = encoder_out_layer(encoder_recurent_1)


#DECODER 
decoder_input = Input(shape=(None,))

decoder_embedding = encoder_embedding_layer(decoder_input)

decoder_recurent_layer_1 = LSTM(LSTM_INTERNAL_DIM, return_sequences=True, return_state=True)
decoder_recurent_1, _, _  = decoder_recurent_layer_1(decoder_embedding, initial_state = [encoder_h, encoder_c])

#decoder_recurent_layer_2 = LSTM(LSTM_INTERNAL_DIM, return_sequences=True, return_state=True)
#decoder_recurent_2, _, _  = decoder_recurent_layer_2(decoder_recurent_1, initial_state = [encoder_h_2, encoder_c_2])

decoder_out_layer = TimeDistributed(Dense(VOC_SIZE, activation='softmax'))
decoder_out = decoder_out_layer(decoder_recurent_1)

total_model = Model([encoder_input, decoder_input], decoder_out)

total_model.load_weights("/en-de/model.h5")


#PREDICT
def predict(model, max_len, x):
    y = [3502]
    while y[-1] != 0 and len(y) < max_len:
        y.append(np.argmax(total_model.predict([x, np.array([y])])[:,-1, :][0]))
    return y

en_w_n = json.load(open("/en-de/en_w_n.json"))
de_n_w = json.load(open("/en-de/de_n_w.json"))

for l in sys.stdin:
	l = l.lower()
	words = l.split(" ")
	words_l = [3502]
	for w in words:
		if w in en_w_n:
			words_l.append(en_w_n[w])
		else:
			words_l.append(3501)

	x = np.array(words_l).reshape(1,-1)


	y = predict(total_model, 30, x)
	#print(y)
	y_w = []
	for w in y[1:]:
		if str(w) in de_n_w:
			y_w.append(de_n_w[str(w)])
		else:
			y_w.append("tykva")

	print(" ".join(y_w))

