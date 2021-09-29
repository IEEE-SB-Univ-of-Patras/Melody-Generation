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
 
maxlen = 9

networkWords = ['0', '1', '2', '3', '4', '5', '6', 
            '7', '8', '9', ' ', 'a']

def CreateNetwork():

   
    notes = sorted(list(set( networkWords )))

    model = keras.Sequential(
    [
        keras.Input(shape=(maxlen, len(notes))),
        layers.LSTM(128),
        layers.Dense(len(notes), activation="softmax"),
    ]
    )

    optimizer = keras.optimizers.RMSprop(learning_rate=0.01)
    model.compile(loss="categorical_crossentropy", optimizer=optimizer)

    return model



def TrainNetwork(model, filename):

    noteString = Processing.MidiFileToString(filename)

    notes = sorted(list(set( networkWords )))

    print(notes)

    note_indices = dict((c, i) for i, c in enumerate(notes))
    indices_note = dict((i, c) for i, c in enumerate(notes))

    # cut the text in semi-redundant sequences of maxlen characters
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
 
    epochs = 40
    batch_size = 128
    
    for epoch in range(epochs):
        model.fit(x, y, batch_size=batch_size, epochs=1,verbose=0)
        print()
        print("Generating text after epoch: %d" % epoch)

        start_index = 0
        for diversity in [0.5]:
            print("Diversity:", diversity)

            generated = ""
            sentence = noteString[start_index : start_index + maxlen]
            print('Generating with seed: "' + sentence + '"')

            for i in range(800):
                x_pred = np.zeros((1, maxlen, len(notes)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, note_indices[char]] = 1.0
                preds = model.predict(x_pred, verbose=0)[0]
                next_index = SampleIndex(preds, diversity)
                next_char = indices_note[next_index]
                sentence = sentence[1:] + next_char
                generated += next_char

            Processing.StringToWav(generated, "RIP_Epoch_{}_Diversity_{}".format(epoch, diversity))
            
            print("Generated: ", generated)

def main():

    Network_DJ = CreateNetwork()

    trainingInput = ["ex3.mid","ex4.mid","ex5.mid"]

    for m in trainingInput:
        TrainNetwork(Network_DJ, m)
        
if __name__ == "__main__":
    main()
