import tkinter as tk

def create_square():
    window = tk.Tk()
    window.title("Kotak Sederhana")

    canvas = tk.Canvas(window, width=200, height=200)
    canvas.pack()

    canvas.create_rectangle(50, 50, 150, 150, fill="blue")

    window.mainloop()

create_square()
