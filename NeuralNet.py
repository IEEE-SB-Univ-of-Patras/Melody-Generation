from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import random

import Processing

def SampleIndex(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)
 

def TrainNetwork():

    noteString = Processing.MidiFileToString("MIDIFILE")


    notes = sorted(list(set( noteString )))

    print(notes)

    print("Total chars: ", len(notes) )

    note_indices = dict((c, i) for i, c in enumerate(notes))
    indices_note = dict((i, c) for i, c in enumerate(notes))

    # cut the text in semi-redundant sequences of maxlen characters
    maxlen = 1
    step = 1
    sentences = []
    next_chars = []
    
    for i in range(0, len(noteString) - maxlen, step):
        sentences.append(noteString[i : i + maxlen])
        next_chars.append(noteString[i + maxlen])
    
    print("Number of sequences:", len(sentences))

    print(sentences)

    x = np.zeros((len(sentences), maxlen, len(notes)), dtype=np.bool)
    y = np.zeros((len(sentences), len(notes)), dtype=np.bool)
    
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            
            x[i, t, note_indices[char]] = 1
       
        y[i, note_indices[next_chars[i]]] = 1
    
    model = keras.Sequential(
    [
        keras.Input(shape=(maxlen, len(notes))),
        layers.LSTM(128),
        layers.Dense(len(notes), activation="softmax"),
    ]
    )
    optimizer = keras.optimizers.RMSprop(learning_rate=0.01)
    model.compile(loss="categorical_crossentropy", optimizer=optimizer)


    epochs = 40
    batch_size = 128
    
    for epoch in range(epochs):
        model.fit(x, y, batch_size=batch_size, epochs=1)
        print()
        print("Generating text after epoch: %d" % epoch)

        start_index = random.randint(0, len(notes) - maxlen - 1)
        for diversity in [0.2, 0.5, 1.0, 1.2]:
            print("...Diversity:", diversity)

            generated = ""
            sentence = noteString[start_index : start_index + maxlen]
            print('...Generating with seed: "' + sentence + '"')

            for i in range(400):
                x_pred = np.zeros((1, maxlen, len(notes)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, note_indices[char]] = 1.0
                preds = model.predict(x_pred, verbose=0)[0]
                next_index = SampleIndex(preds, diversity)
                next_char = indices_note[next_index]
                sentence = sentence[1:] + next_char
                generated += next_char

            generated = Processing.StringToNotes(generated)
            
            Processing.StringToWav(generated, "Epoch_{}".format(epoch))
            
            print("...Generated: ", generated)

