from frontend.constants import *
from App import StateApp
from tkinter import *

root = Tk()
root.geometry(f"{windowWidth}x{windowHeight}")
root.title("Crichopper UI")

if __name__ == '__main__':
    # initializing app object
    app = StateApp(root)
    # starting app thread loop
    app.initiator().mainloop()