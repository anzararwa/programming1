from tkinter import *

window = Tk()
window.geometry("350x200")
window.title("COMP1753 GUI")
chk_state = BooleanVar()
chk_state.set(True)

chk = Checkbutton(window, text="choose", var=chk_state)
chk.grid(column=0, row=0)

def clicked():
    if chk_state.get():
       res = "Checkbox is checked"
    else:
        res = "Checkbox is checked"
    output.set(res)

btn = Button(window, text="Click Me", command=clicked)
btn.grid(column=1, row=0)

output = StringVar()

txt = Entry(window, width=10, textvariable=output, state="readonly")


window.mainloop()