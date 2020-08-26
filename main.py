from tkinter import *
import build_classifier



def predict():
    global tag
    tag = build_classifier.predict(e1.get())



if __name__ == '__main__':

    master = Tk()
    master.title('Election Predictor')
    photo = PhotoImage(file="1077613_I.gif")
    canvas = Canvas(master, width=photo.width(), height=photo.height())
    canvas.pack()
    canvas.create_image(0, 0, image=photo, anchor='nw')

    Label(master, text = "Friend's user Name", font='Helvetica 20 bold italic').place(x = 225, y= 150)
    e1 = Entry(master)
    e1.place(x = 225, y= 200)
    b = Button(master, text="Submit",font='Helvetica 20 bold italic' , command=predict)
    b.place(x = 275, y= 250)

    master.mainloop()

    if tag == 'Right':
        popup = Tk()
        popup.title('Right Voter')
        photo1 = PhotoImage(file="bibi.gif")
        label = Canvas(popup, width=photo1.width(), height=photo1.height())
        label.pack()
        label.create_image(0, 0, image=photo1, anchor='nw')
        popup.mainloop()

    else:
        popup2 = Tk()
        popup2.title('Left-Center Voter')
        photo2 = PhotoImage(file="benny.gif")
        label2 = Canvas(popup2, width=photo2.width(), height=photo2.height())
        label2.pack()
        label2.create_image(0, 0, image=photo2, anchor='nw')
        popup2.mainloop()
