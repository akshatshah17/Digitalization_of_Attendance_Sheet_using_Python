import cv2
import datetime
import imutils
from imutils import contours
import numpy as np
import csv
import os
from tkinter import *
from tkinter import filedialog, messagebox

fl = 0
mainflag1 = 0
mainflag2 = 0

# SPECIFY THE PATH WHERE FILES SHOULD BE STORED (END WITH THIS / or // or \ or \\ AS REQUIRED) This needs to change according to users choice
fname1 = "D:\\Study\\Python\\Project\\CSV\\"


# FUNCTION TO IMPLEMENT ADD DATA
def add_data():
    # TAKING IMAGE OF ATTENDANCE SHEET
    try:
        mainWindow = Tk()
        mainWindow.sourceFile = filedialog.askopenfilename(
            filetypes=(("ImageFiles", ("*.jpg", "*.png", "*.jpeg")), ("All Files", "*")), parent=mainWindow,
            title="Please select an image")
        img_path = mainWindow.sourceFile
        mainWindow.destroy()

        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 100, 200)

        # FINDING ALL CONTOURS FROM IMAGE
        cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        # FINDING ONLY BUBBLED CONTOURS
        cntbubble = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            if w >= 40 and h >= 40 and ar <= 1.1:
                cntbubble.append(c)

        # SORTING ALL THOSE BUBBLED CONTOURS
        cntbubble = contours.sort_contours(cntbubble, method="top-to-bottom")[0]

        # OBTAINING THRESH IMAGE TO DETECT BLACK AND WHITE SPOTS
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # 30 STUDENTS LIST OF ATTENDANCE
        attend = []
        for i in range(30):
            attend.append([])

        x = 0
        for i in range(0, len(cntbubble), 5):

            # SORTING ROWWISE BUBBLED CONTOURS
            temp = contours.sort_contours(cntbubble[i:i + 5])[0]

            for (j, c) in enumerate(temp):

                # INITIALIZING MASK WITH ALL 0
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)

                # FINDING PIXEL BY PIXEL TO CHECK BLACK SPOT IN CONTOUR
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                pixel = cv2.countNonZero(mask)

                # APPENDING A OR P IN ATTENDANCE FOR RESPECTIVE STUDENT
                if pixel > 100:
                    attend[x].append("A")
                else:
                    attend[x].append("P")

            x += 1

    except:
        global mainflag1
        mainflag1 = 1

    # CHECKING IF IMAGE IS UPLOADED OR NOT
    if mainflag1 == 0:

        # INPUTING FILE NAME  AND DATES TO WRITE
        def validate(day, month, year):
            isValidDate = True
            try:
                datetime.datetime(int(year), int(month), int(day))
            except ValueError:
                isValidDate = False
            return isValidDate

        # CHECKING ALL INPUTS ARE VALID
        while fl == 0:

            root1 = Tk()
            root1.geometry('820x650+500+0')

            def on_closing():
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                    global fl
                    fl = 1
                    global mainflag2
                    mainflag2 = 1
                    root1.destroy()

            def clicked(b, s, d1, d2, d3, d4, d5):
                try:
                    global inp
                    inp = s + "_" + b
                    dat1 = 0
                    dat2 = 0
                    dat3 = 0
                    dat4 = 0
                    dat5 = 0
                    flagb = 0
                    flags = 0
                    flagerror = 0
                    global date1, date2, date3, date4, date5
                    dmy1 = d1.split('/')
                    dmy2 = d2.split('/')
                    dmy3 = d3.split('/')
                    dmy4 = d4.split('/')
                    dmy5 = d5.split('/')

                    if b != "":
                        flagb = 1
                    else:
                        myLabel6.configure(text="\nPlease select Batch.")
                        flagerror = 1

                    if s != "":
                        flags = 1
                    else:
                        myLabel6.configure(text="\nPlease Insert Subject.")
                        flagerror = 1

                    if validate(dmy1[0], dmy2[1], dmy3[2]):
                        date1 = d1
                        dat1 = 1
                    else:
                        myLabel6.configure(text="\nDate 1 is not valid.")
                        flagerror = 1

                    if validate(dmy2[0], dmy2[1], dmy2[2]):
                        date2 = d2
                        dat2 = 1
                    else:
                        myLabel6.configure(text="\nDate 2 is not valid.")
                        flagerror = 1

                    if validate(dmy3[0], dmy3[1], dmy3[2]):
                        date3 = d3
                        dat3 = 1
                    else:
                        myLabel6.configure(text="\nDate 3 is not valid.")
                        flagerror = 1

                    if validate(dmy4[0], dmy4[1], dmy4[2]):
                        date4 = d4
                        dat4 = 1
                    else:
                        myLabel6.configure(text="\nDate 4 is not valid.")
                        flagerror = 1

                    if validate(dmy5[0], dmy5[1], dmy5[2]):
                        date5 = d5
                        dat5 = 1
                    else:
                        myLabel6.configure(text="\nDate 5 is not valid.")
                        flagerror = 1

                    if flagb == 1 and flags == 1 and dat1 == 1 and dat2 == 1 and dat3 == 1 and dat4 == 1 and dat5 == 1:
                        myLabel6.configure(text="\nAll inputs are valid.")
                        global fl
                        fl = 1
                        root1.destroy()

                    elif flagerror == 0:
                        myLabel6.configure(text="\nPlease enter valid inputs.")

                except:
                    myLabel6.configure(text="\nInvalid Input.")

            # GUI WINDOW FOR TAKING INPUT
            myLabel = Label(root1, text="Choose batch", font=("ArailBold", 15))
            myLabel.pack()

            batch = StringVar(root1)
            batch.set("0")

            Radiobutton(root1, text="Batch 1", font=("ArailBold", 15), variable=batch, value="1").pack()
            Radiobutton(root1, text="Batch 2", font=("ArailBold", 15), variable=batch, value="2").pack()

            myLabel = Label(root1, text="Enter subject name", font=("ArailBold", 15))
            myLabel.pack()
            subject = Entry(root1)
            subject.pack()

            Label(root1, text="\nDate Format : dd/mm/yyyy", font=("ArailBold", 15)).pack()
            myLabel1 = Label(root1, text="Enter Date 1", font=("ArailBold", 15))
            myLabel1.pack()
            da1 = Entry(root1)
            da1.pack()

            myLabel2 = Label(root1, text="Enter Date 2", font=("ArailBold", 15))
            myLabel2.pack()
            da2 = Entry(root1)
            da2.pack()

            myLabel3 = Label(root1, text="Enter Date 3", font=("ArailBold", 15))
            myLabel3.pack()
            da3 = Entry(root1)
            da3.pack()

            myLabel4 = Label(root1, text="Enter Date 4", font=("ArailBold", 15))
            myLabel4.pack()
            da4 = Entry(root1)
            da4.pack()

            myLabel5 = Label(root1, text="Enter Date 5", font=("ArailBold", 15))
            myLabel5.pack()
            da5 = Entry(root1)
            da5.pack()

            myLabel7 = Label(root1, text="\n").pack()
            Button(root1, text="CONFIRM", padx=55, pady=5,
                   command=lambda: clicked(batch.get(), subject.get(), da1.get(), da2.get(), da3.get(), da4.get(),
                                           da5.get()), bg="green", fg="white", font=("Arial Bold", 15)).pack()
            Button(root1, text="QUIT", padx=55, pady=5, command=on_closing, bg="red", fg="white",
                   font=("Arial Bold", 15)).pack()

            myLabel6 = Label(root1, text="\n", font=("ArailBold", 15))
            myLabel6.pack()
            root1.mainloop()

    else:
        pass

    # CHECKING BOTH CONDITIONS (PHOTO UPLOADED AND ALL VALID INPUTS)
    if mainflag1 == 0 and mainflag2 == 0:

        global fname1
        filename1 = fname1 + inp + ".csv"

        prevattend = []

        # READING DATA FROM CSV FILE IF ALREADY EXISTS EARLIER
        if os.path.exists(filename1):
            with open(filename1, 'r') as csvfile:
                cr = csv.reader(csvfile)
                titleread = next(cr)

                for row in cr:
                    if len(row) != 0:
                        prevattend.append(row[1:])

            titleread.extend([date1, date2, date3, date4, date5])

        else:
            titleread = ["Roll No.", date1, date2, date3, date4, date5]

        title = titleread
        rows = []

        for i in range(30):
            makerow = [i + 1]
            if len(prevattend) != 0:
                makerow.extend(prevattend[i])
            makerow.extend(attend[i])
            rows.append(makerow)

        # WRITING DATA IN CSV FILE
        with open(filename1, 'w') as csvfile:
            cw = csv.writer(csvfile)
            cw.writerow(title)

            for i in range(30):
                cw.writerow(rows[i])

    else:
        pass


# FUNCTION TO IMPLEMENT DISPLAY DATA
def display_data():
    # GUI FOR TAKING INPUT
    window = Tk()
    window.title("Available Functions")
    window.geometry('820x650+500+0')

    optionVar = StringVar()
    optionVar.set("DROP DOWN MENU")
    Label(window, text="Please open below drop down menu.\n", padx=25, pady=40, font=("Arial Bold", 15)).pack(
        anchor=CENTER)
    option = OptionMenu(window, optionVar, "1.Role number vise attendance\n",
                        "2.Date vise attendence\n",
                        "3.Students who have attendance more than 85%.\n",
                        "4.Students who have attendance less than 65%.\n",
                        "5.Students who have attendance b.w 65% and 85%.\n")
    option.pack()

    def on_closingfunchoise():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()

    def show():
        valu = optionVar.get()

        global fname1

        # IMPLEMENTATION OF FUNCTION 1
        if valu[0] == '1':

            myLabel.configure(text="\n" + valu + " will be shown on another window.")
            root = Tk()
            root.geometry('500x400')

            def clickedbut(bat, sub, r):

                f1 = sub + "_" + bat
                filename = fname1 + f1 + ".csv"

                try:
                    with open(filename, 'r') as csvfile:
                        csvreader = csv.reader(csvfile)
                        fields = next(csvreader)
                        x = 1
                        a = list()
                        for row in csvreader:
                            if x % 2 == 0:
                                a.append(row)
                            x += 1
                        num = r
                        if num.isnumeric():
                            e = 0
                            for b in a:
                                if b[0] == num:
                                    e = 1
                                    tot = len(b) - 1
                                    pre = b.count('P')
                                    per = (100 * pre) / tot
                                    Label(root, text="Student with roll number " + str(num) + " has " + str(
                                        per) + " % attendance.").pack()
                                    Label(root, text="Student's data").pack()
                                    Label(root, text=fields).pack()
                                    Label(root, text=b).pack()
                            if e == 0:
                                Label(root, text="Roll number not found.").pack()
                        else:
                            Label(root, text="Invalid roll number.").pack()

                except FileNotFoundError:
                    Label(root, text="File not found.").pack()

                return

            Label(root, text="Choose batch").pack()

            batch = StringVar(root)
            batch.set("1")

            Radiobutton(root, text="Batch 1", variable=batch, value="1").pack()
            Radiobutton(root, text="Batch 2", variable=batch, value="2").pack()

            Label(root, text="Enter subject name").pack()
            subject = Entry(root)
            subject.pack()
            Label(root, text="Enter roll number").pack()
            roll = Entry(root)
            roll.pack()
            Button(root, text="Submit", command=lambda: clickedbut(batch.get(), subject.get(), roll.get())).pack()
            Button(root, text="Quit", command=root.destroy).pack()
            root.mainloop()

        # IMPLEMENTATION OF FUNCTION 2
        elif valu[0] == '2':

            myLabel.configure(text="\n" + valu + " will be shown on another window.")
            root = Tk()
            root.geometry('500x800')

            def clickedbut(bat, sub, d):

                f1 = sub + "_" + bat
                filename = fname1 + f1 + ".csv"

                try:
                    with open(filename, 'r') as csvfile:
                        csvreader = csv.reader(csvfile)
                        fields = next(csvreader)
                        x = 1
                        a = list()
                        for row in csvreader:
                            if x % 2 == 0:
                                a.append(row)
                            x += 1
                        e = 0
                        f = 0
                        da = d
                        for words in fields:
                            e += 1
                            if words == da:
                                f = 1
                                break
                        if f == 1:
                            Label(root, text="Here is the details of date: " + da).pack()
                            Label(root, text="Roll no - (P/A)").pack()
                            for i in range(len(a) // 2):
                                Label(root,
                                      text=a[i][0] + " - " + a[i][e - 1] + "\t" + a[i + 15][0] + " - " + a[i + 15][
                                          e - 1]).pack()
                        else:
                            Label(root, text="Date not found.").pack()

                except FileNotFoundError:
                    Label(root, text="File not found.").pack()

                return

            Label(root, text="Choose batch").pack()

            batch = StringVar(root)
            batch.set("1")

            Radiobutton(root, text="Batch 1", variable=batch, value="1").pack()
            Radiobutton(root, text="Batch 2", variable=batch, value="2").pack()

            Label(root, text="Enter subject name").pack()
            subject = Entry(root)
            subject.pack()
            Label(root, text="Enter Date").pack()
            date = Entry(root)
            date.pack()
            Button(root, text="Submit", command=lambda: clickedbut(batch.get(), subject.get(), date.get())).pack()
            Button(root, text="Quit", command=root.destroy).pack()
            root.mainloop()

        # IMPLEMENTATION OF FUNCTION 3
        elif valu[0] == '3':

            myLabel.configure(text="\n" + valu + " will be shown on another window.")
            root = Tk()
            root.geometry('500x800')
            root.resizable(width=True, height=True)

            def clickedbut(bat, sub):

                f1 = sub + "_" + bat
                filename = fname1 + f1 + ".csv"
                ans = list()

                try:
                    with open(filename, 'r') as csvfile:
                        csvreader = csv.reader(csvfile)
                        fields = next(csvreader)
                        x = 1
                        a = list()
                        for row in csvreader:
                            if x % 2 == 0:
                                a.append(row)
                            x += 1
                        for b in a:
                            tot = len(b) - 1
                            pre = b.count('P')
                            per = (100 * pre) / tot
                            if per >= 85:
                                ans.append(b)

                        Label(root, text="Here is the details of student who has more than 85% attendance:").pack()
                        Label(root, text="Total number of students: " + str(len(ans))).pack()
                        Label(root, text=fields).pack()
                        for r in ans:
                            Label(root, text=r).pack()

                except FileNotFoundError:
                    Label(root, text="File not found.").pack()

                return

            Label(root, text="Choose batch").pack()

            batch = StringVar(root)
            batch.set("1")

            Radiobutton(root, text="Batch 1", variable=batch, value="1").pack()
            Radiobutton(root, text="Batch 2", variable=batch, value="2").pack()

            Label(root, text="Enter subject name").pack()
            subject = Entry(root)
            subject.pack()
            Button(root, text="Submit", command=lambda: clickedbut(batch.get(), subject.get())).pack()
            Button(root, text="Quit", command=root.destroy).pack()
            root.mainloop()

        # IMPLEMENTATION OF FUNCTION 4
        elif valu[0] == '4':

            myLabel.configure(text="\n" + valu + " will be shown on another window.")
            root = Tk()
            root.geometry('500x800')
            root.resizable(width=True, height=True)

            def clickedbut(bat, sub):

                f1 = sub + "_" + bat
                filename = fname1 + f1 + ".csv"
                ans = list()

                try:
                    with open(filename, 'r') as csvfile:
                        csvreader = csv.reader(csvfile)
                        fields = next(csvreader)
                        x = 1
                        a = list()
                        for row in csvreader:
                            if x % 2 == 0:
                                a.append(row)
                            x += 1
                        for b in a:
                            tot = len(b) - 1
                            pre = b.count('P')
                            per = (100 * pre) / tot
                            if per < 65:
                                ans.append(b)

                        Label(root, text="Here is the details of student who has less than 65% attendance:").pack()
                        Label(root, text="Total number of students: " + str(len(ans))).pack()
                        Label(root, text=fields).pack()
                        for r in ans:
                            Label(root, text=r).pack()

                except FileNotFoundError:
                    Label(root, text="File not found.").pack()

                return

            Label(root, text="Choose batch").pack()

            batch = StringVar(root)
            batch.set("1")

            Radiobutton(root, text="Batch 1", variable=batch, value="1").pack()
            Radiobutton(root, text="Batch 2", variable=batch, value="2").pack()

            Label(root, text="Enter subject name").pack()
            subject = Entry(root)
            subject.pack()
            Button(root, text="Submit", command=lambda: clickedbut(batch.get(), subject.get())).pack()
            Button(root, text="Quit", command=root.destroy).pack()
            root.mainloop()

        # IMPLEMENTATION OF FUNCTION 5
        elif valu[0] == '5':

            myLabel.configure(text="\n" + valu + " will be shown on another window.")
            root = Tk()
            root.geometry('500x800')
            root.resizable(width=True, height=True)

            def clickedbut(bat, sub):

                f1 = sub + "_" + bat
                filename = fname1 + f1 + ".csv"
                ans = list()

                try:
                    with open(filename, 'r') as csvfile:
                        csvreader = csv.reader(csvfile)
                        fields = next(csvreader)
                        x = 1
                        a = list()
                        for row in csvreader:
                            if x % 2 == 0:
                                a.append(row)
                            x += 1
                        for b in a:
                            tot = len(b) - 1
                            pre = b.count('P')
                            per = (100 * pre) / tot
                            if 65 <= per < 85:
                                ans.append(b)

                        Label(root,
                              text="Here is the details of student whose attendance in between 65% and 85%:").pack()
                        Label(root, text="Total number of students: " + str(len(ans))).pack()
                        Label(root, text=fields).pack()
                        for r in ans:
                            Label(root, text=r).pack()

                except FileNotFoundError:
                    Label(root, text="File not found.").pack()

                return

            Label(root, text="Choose batch").pack()

            batch = StringVar(root)
            batch.set("1")

            Radiobutton(root, text="Batch 1", variable=batch, value="1").pack()
            Radiobutton(root, text="Batch 2", variable=batch, value="2").pack()

            Label(root, text="Enter subject name").pack()
            subject = Entry(root)
            subject.pack()
            Button(root, text="SUBMIT", command=lambda: clickedbut(batch.get(), subject.get())).pack()
            Button(root, text="QUIT", command=root.destroy).pack()
            root.mainloop()

        else:
            Label(window, text="Please select any one.\n", padx=25, pady=40, font=("Arial Bold", 15)).pack(
                anchor=CENTER)

    Button(window, text="CONFIRM", padx=55, pady=5, command=show, bg="green", fg="white",
           font=("Arial Bold", 15)).pack()
    Button(window, text="QUIT", padx=55, pady=5, command=on_closingfunchoise, bg="red", fg="white",
           font=("Arial Bold", 15)).pack()
    myLabel = Label(window, text="\n", font=("Arail Bold", 15))
    myLabel.pack()

    window.mainloop()


# MAIN FUNCTION
def cls():
    def on_closingmain():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            mainWin.destroy()

    def val(ch):

        if ch == 1:
            mainWin.destroy()
            add_data()
            global fl
            fl = 0
            global mainflag2
            mainflag2 = 0
            global mainflag1
            mainflag1 = 0
            global date1
            date1 = " "
            global date2
            date2 = " "
            global date3
            date3 = " "
            global date4
            date4 = " "
            global date5
            date5 = " "
            cls()

        elif ch == 2:
            mainWin.destroy()
            display_data()
            cls()

        else:
            Label(mainWin, text="Please select any one option from drop down menu.\n", padx=25, pady=40,
                  font=("Arial Bold", 15)).pack(anchor=CENTER)

    # MAIN GUI WINDOW
    mainWin = Tk()
    mainWin.title("Python-Project")
    mainWin.geometry("400x385+100+200")
    mainWin.resizable(0, 0)

    v = IntVar()
    v.set(0)
    Label(mainWin, text="Please select below one of the following.\n", padx=25, pady=20, font=("Arial Bold", 15)).pack(
        anchor=CENTER)
    Radiobutton(mainWin, text="1.ADD DATA\n", variable=v, value=1, padx=55, font=("Arial Bold", 15), fg="blue").pack(
        anchor=CENTER)
    Radiobutton(mainWin, text="2.DISPLAY DATA\n", variable=v, value=2, padx=55, font=("Arial Bold", 15),
                fg="blue").pack(anchor=CENTER)
    Button(mainWin, text="CONFIRM", padx=55, pady=5, command=lambda: val(v.get()), bg="green", fg="white",
           font=("Arial Bold", 15)).pack()
    Button(mainWin, text="QUIT", padx=55, pady=5, command=on_closingmain, bg="red", fg="white",
           font=("Arial Bold", 15)).pack()
    Label(mainWin, text='\n\nDeveloped by :\n "Akshat Shah, Devam Shah, Parth Shah"', font=("Arial Italic",11)).pack(anchor=SW)
    mainWin.mainloop()


cls()
