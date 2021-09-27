import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import ImageTk, Image

class MelodyGenerationApp():

    def __init__(self, root):

        self.root = root

        root.title("Melody Generation")

        self.canvas = tk.Canvas(root, width=1000, height=700)
        self.canvas.place(x=0, y=0, anchor=tk.NW)

        self.font = "SourceCodePro"

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
                                     outline="#3db9bb", fill="#3db9bb") 
        
        self.canvas.create_text(70, 50, text = "Melody Generation :)",
                                anchor = tk.NW,  font = self.font + " 30")

    def placeButtons(self):

        def loadMidis():

            filetypes = (
                    ('MIDI Files', '*.mid'),
                    ('All files', '*.*')
                )

            selectedMidis = filedialog.askopenfilenames(filetypes=filetypes)

            print(selectedMidis)
        
        loadButton = tk.Button(text="Load MIDIs", font = self.font + " 10", 
                               command = lambda: loadMidis()) 
        loadButton.place(x=60, y= 380)

        


def main():

    root = tk.Tk()
    app = MelodyGenerationApp(root)
    root.mainloop()

main()
