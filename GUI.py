import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import ImageTk, Image
import threading

import NeuralNet

class MelodyGenerationApp():

    def __init__(self, root):

        self.root = root

        root.title("Melody Generation")

        self.canvas = tk.Canvas(root, width=1000, height=700)
        self.canvas.place(x=0, y=0, anchor=tk.NW)

        self.font = "SourceCodePro"

        self.selectedMidis = []

        self.drawLogo()

        self.placeButtons()


    def drawLogo(self):
        
        x, y = 40, 10
        w, h = 600, 100
        x_ = x + 20
        y_ = y + 20


        self.canvas.create_rectangle(x, y, x+w, y+h, 
                                     outline="#10b8bb", fill="#10b8bb") 
        self.canvas.create_rectangle(x_, y_, x_+w, y_+h, 
                                     outline="#66bb10", fill="#66bb10") 
        self.canvas.create_rectangle(x , y_ + h + 10, x_+1*w, y_+4*h,   
                                     outline="#3db9bb", fill="#3db9bb") # Big rectangle
        
        self.canvas.create_text(70, 50, text = "Melody Generation :)",
                                anchor = tk.NW,  font = self.font + " 30")

    def placeButtons(self):

        def loadMidis():

            filetypes = (
                    ('MIDI Files', '*.mid'),
                    ('All files', '*.*')
                )

            self.selectedMidis = filedialog.askopenfilenames(filetypes=filetypes)

            loadedString = "\n".join(["• {}".format(midi.split("/")[-1]) for midi in self.selectedMidis])

            loadedLabel = tk.Label(text="MIDIs loaded: " + "\n" + loadedString, font = self.font + " 10", bg = "#3db9bb", justify = "left")
            loadedLabel.place(x=40, y=140)

        loadButton = tk.Button(text="Load MIDIs", font = self.font + " 10", 
                               command = lambda: loadMidis()) 

        trainButton = tk.Button(text="Create Music", font = self.font + " 10",
                                command = lambda: self.startNeuralNetwork())
        quitButton = tk.Button(text="Quit", font = self.font + " 10", fg = "red", command = self.root.destroy)

        loadButton.place(x=260, y= 380)
        trainButton.place(x=60, y= 380)
        quitButton.place(x=460, y=380)

    def startNeuralNetwork(self):
        
        Network_DJ = NeuralNet.CreateNetwork()
        
        def doTrain():
            for m in self.selectedMidis:
                NeuralNet.TrainNetwork(Network_DJ, m)

        threading.Thread(target=doTrain).start()


def main():

    root = tk.Tk()
    app = MelodyGenerationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
