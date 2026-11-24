from atexit import _clear
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

window = Tk()
window.geometry("350x200")
window.title("Student Registration Form")

lbl_name = Label(window, text="Full Name:")
lbl_name.grid(column=0, row=0)

input_name = Entry(window, width=20)
input_name.grid(column=1, row=0)

lbl_age = Label(window, text="Age:")
lbl_age.grid(column=0, row=1)

input_age = Entry(window, width=20)
input_age.grid(column=1, row=1)

lbl_gender = Label(window, text="Gender:")
lbl_gender.grid(column=0, row=2)

gender_var = IntVar(value=0)

rad1 = Radiobutton(window, text="Male", variable=gender_var, value=1)
rad1.grid(column=1, row=2)
rad2 = Radiobutton(window, text="Female", variable=gender_var, value=2)
rad2.grid(column=2, row=2)

lbl_course = Label(window, text="Course:")
lbl_course.grid(column=0, row=3)

combo_course = ttk.Combobox(window, width=15)
combo_course['values'] = ("BTEC IT", "BTEC BUSINESS", "ABE", "ACCA")
combo_course.grid(column=1, row=3)

lbl_email = Label(window, text="Email:")
lbl_email.grid(column=0, row=4)

input_email = Entry(window, width=20)
input_email.grid(column=1, row=4)

chk_state = BooleanVar()
chk_state.set(False)

chk = Checkbutton(window, text="Confirmation?", variable=chk_state)
chk.grid(column=0, row=5)

def submit():
    if chk_state.get() == False:
        messagebox.showwarning("Warning", "Please check the confirmation box before submitting.")
    else:
        lbl_submit.configure(text="Submitted!")
        messagebox.showinfo("Success", "Student registration details submitted successfully!")

btn_submit = Button(window, text="Submit", command=submit)
btn_submit.grid(column=0, row=6)

lbl_submit = Label(window, text="Submit")
lbl_submit.grid(column=1, row=6)

def clear():
    lbl_clear.configure(text="Cleared!")
    input_name.delete(0, END)
    input_age.delete(0, END)
    input_email.delete(0, END)
    combo_course.set("")
    gender_var.set(0)
    chk_state.set(False)

btn_clear = Button(window, text="Clear", command=clear)
btn_clear.grid(column=0, row=7, pady=10)

lbl_clear = Label(window, text="Clear")
lbl_clear.grid(column=1, row=7)






window.mainloop()