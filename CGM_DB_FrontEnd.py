import tkinter
from tkinter import *
import io
import tkinter.messagebox
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from datetime import date
from PIL import ImageTk, Image
from tkinter.scrolledtext import *
import os
import csv
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
from matplotlib.dates import datetime as dt

import CGM_DB_BackEnd
import CGM_DB_Attendance_Backend


def main():
    root = Tk()
    app = Login(root)
    root.withdraw()
    root.mainloop()


class Login:
    def __init__(self, master):
        self.master = master
        self.master = Toplevel()
        self.master.title("CGM Database Management System")
        get_width = self.master.winfo_screenwidth()
        get_height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (get_width, get_height))
        self.bring_backlogin()

        def Login_System():
            user = (self.Username.get())
            pas = (self.Password.get())

            if user == '' or pas == '':
                messagebox.showerror("CGM Database Management System", "All fields are required !!")

            elif (user == "admin" and pas == "conquerors"):
                self.master.withdraw()
                Main_window()
            else:
                messagebox.showerror("CGM Database Management System", "Invalid Username or Password !!")

        def Main_window():
            self.MainWindow = Toplevel(self.master)
            self.app = Member(self.MainWindow)

        # ===========Top Title Frame ====================
        # NB: This Frame is common to all Tabs / Notebook pages
        TitleFrame = Frame(self.master, bd=2, padx=10, pady=8, bg="Ghost white", relief=RIDGE)
        TitleFrame.pack(fill=X, side=TOP)

        CGM_logo = Image.open("CGM_logo.jpg")
        CGM_logo_resized = CGM_logo.resize((100, 100), Image.ANTIALIAS)
        CGM_Logo = ImageTk.PhotoImage(CGM_logo_resized)
        self.lblLogo = Label(TitleFrame, image=CGM_Logo, padx=20)
        self.lblLogo.image = CGM_Logo
        self.lblLogo.grid(row=0, column=0, padx=40, sticky=W)

        self.lblTit = Label(TitleFrame, font=('arial', 40, 'bold'), text="CGM Database Management System",
                            bg="Ghost white", padx=50)
        self.lblTit.grid(row=0, column=1, padx=20)
        # =======================================================
        # login variables
        self.Username = StringVar()
        self.Password = StringVar()

        self.Username.set("admin")  # remove code after testing period
        self.Password.set("conquerors")  # remove code after testing period

        self.frame = Frame(self.master)
        self.frame.pack(side=BOTTOM)

        # images for login window
        self.bg_icon = ImageTk.PhotoImage(file="login_background.jpg")
        self.user_icon = PhotoImage(file="user_icon.png")
        self.pass_icon = PhotoImage(file="pass_icon.png")
        self.logo_icon = PhotoImage(file="logo_icon.png")

        lbl_background = Label(self.frame, text="welcome Holy Spirit", image=self.bg_icon, compound=CENTER).pack()

        login_frame = Frame(self.frame, bg="white")
        login_frame.place(x=get_width * 0.35, y=get_height * 0.16)
        # login_frame.bind('<Return>', Login_System)

        lbl_logo = Label(login_frame, image=self.logo_icon, bg="white", bd=0).grid(row=0, pady=20, columnspan=2)
        lbl_user = Label(login_frame, text="Username", image=self.user_icon, compound=LEFT,
                         font=("Calibri", 18, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=10)
        txt_user = Entry(login_frame, bd=5, relief=GROOVE, textvariable=self.Username, font=("", 15))
        txt_user.grid(row=1, column=1, padx=20)
        txt_user.focus()
        lbl_user = Label(login_frame, text="Password", image=self.pass_icon, compound=LEFT,
                         font=("Calibri", 18, "bold"), bg="white").grid(row=2, column=0, padx=10, pady=10)
        txt_pass = Entry(login_frame, bd=5, relief=GROOVE, textvariable=self.Password, font=("", 15))
        txt_pass.grid(row=2, column=1, padx=20)
        btn_login = Button(login_frame, text="Login", width=15, font=("Calibri", 14, "bold"), bg="cornflower blue",
                           relief=GROOVE, command=Login_System)
        btn_login.grid(row=3, column=1, pady=10)

        txt_user.bind('<Return>', lambda event=None: btn_login.invoke())  # Enter key retuns btn_login command
        txt_pass.bind('<Return>', lambda event=None: btn_login.invoke())  # Enter key retuns btn_login command

    # reloads login screen after logout. Called by logout Btn
    def bring_backlogin(self):
         # self.master.update()
         self.master.deiconify()

class Member:
    def __init__(self, root):
        self.root = root
        self.root.title("CGM Database Management System")
        get_width = self.root.winfo_screenwidth()
        get_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (get_width, get_height))
        self.root.state('zoomed')

        # log out function
        def logout():
            x = messagebox.askquestion("CGM Database Management System", "Your session will be logged out \nDo you like to continue ?")
            if x == 'yes':
                self.root.destroy()
                class LoginAgain (Login):  # creates a child class of Login class
                     pass
                y = LoginAgain(self)  # instantiates LoginAgain class
                y.bring_backlogin()   # reloads login page
            else:
                pass

        # ===========Top Title Frame ====================
        # NB: This Frame is common to all Tabs / Notebook pages
        TitleFrame = Frame(self.root, bd=2, padx=10, pady=8, bg="Ghost white", relief=RIDGE)
        TitleFrame.pack(fill=X, side=TOP)  # expand=True,

        CGM_logo = Image.open("CGM_logo.jpg")
        CGM_logo_resized = CGM_logo.resize((100, 100), Image.ANTIALIAS)
        CGM_Logo = ImageTk.PhotoImage(CGM_logo_resized)
        self.lblLogo = Label(TitleFrame, image=CGM_Logo, padx=20)
        self.lblLogo.image = CGM_Logo
        self.lblLogo.grid(row=0, column=0, padx=40, sticky=W)

        self.lblTit = Label(TitleFrame, font=('arial', 40, 'bold'), text="CGM Database Management System",
                            bg="Ghost white", padx=50)
        self.lblTit.grid(row=0, column=1, padx=20)

        self.btnLogout = Button(TitleFrame, text='Logout', font=('arial', 12, 'bold'), height=1, width=11,
                                bd=4, bg='orange red', command=logout, cursor='hand2')
        self.btnLogout.grid(row=0, column=2, padx=(200, 10), pady=10, sticky=E)

        # ==========Notebook / Tabs============
        style = ttk.Style(self.root)
        style.configure("lefttab.TNotebook.Tab", padding=[40, 40], font=('arial', 11))
        style.configure("lefttab.TNotebook", tabposition='wn')
        style.map("lefttab.TNotebook.Tab")

        # Tab Layout
        my_notebook = ttk.Notebook(self.root, style='lefttab.TNotebook')
        my_notebook.pack(side=BOTTOM, expand=1, fill="both")

        home_tab = ttk.Frame(my_notebook)
        view_tab = ttk.Frame(my_notebook)
        attendance_tab = ttk.Frame(my_notebook)

        # Adds Tabs to Notebook
        my_notebook.add(home_tab, text=f'{"Home":^13s}')
        my_notebook.add(view_tab, text=f'{"View":^15s}')
        my_notebook.add(attendance_tab, text=f'{"Attendance":^4s}')

        # variables
        Prefix = StringVar()
        Firstname = StringVar()
        Surname = StringVar()
        MiddleName = StringVar()
        ChurchPosition = StringVar()
        Department = StringVar()
        LocalCenter = StringVar()
        DoB = StringVar()
        Age = StringVar()  # check if there's the need to change to IntVar()
        Gender = StringVar()
        Res_Address = StringVar()
        City = StringVar()
        Region = StringVar()
        Country = StringVar()
        Nationality = StringVar()
        MaritalStatus = StringVar()
        Mobile = StringVar()
        Telephone = StringVar()
        Email = StringVar()
        Education = StringVar()
        Occupation = StringVar()
        ChurchStatus = StringVar()

        # lists for Combo boxes with longer list of options
        Regions = ["Select Region", "Western", "Western-North", "Greater Accra", "Ashanti", "Brong Ahafo",
                   "Bono-East", "Ahafo", "Central", "Eastern", "Northern", "Savannah", "North East",
                   "Upper East", "Upper West", "Volta", "Oti", "N/A"]

        Positions = ["Select Position", "Apostle", "Reverend", "Minister", "Elder", "Deacon",
                     "Lady Deacon", "Shepherd", "Ass. Shepherd", "member"]

        Departments = ["Select Department", "Blessed Choir", "Technical", "Ushering",
                       "Protocol", "Hospitality", "Children's Dept", "N/A"]

        LocalCenters = ["Select Local Center", "Whindo", "Assakae", "Lagos town", "Kwesimitsim - zongo",
                        "Kwesimitsim - main", "Anaji", "Takoradi - Number 2", "Takoradi -main", "Kweikuma", "Sekondi",
                        "Bakaekyir", "Mempeasem", "Mpintsin", "Accra", "Kumasi", "Wemfie", "N/A"]

        Education_levels = ["Select Education Level", "Basic", "Junior High", "Senior High", "Bachelors", "Masters",
                            "PhD", "Post-Doc", "Other"]

        # ===============Functions=================
        # FUNCTIONS FOR HOME TAB
        def iExit():
            iExit = tkinter.messagebox.askyesno("CGM Database Management System", "Confirm if you want to exit",
                                                parent=root)
            if iExit > 0:
                root.quit()
                return

        # de-highlights combo boxes
        def defocus(event):
            event.widget.master.focus_set()

        # For Clear Entry button
        def clearData():
            try:
                self.Prefix_combo.current(0)
                self.txtF_name.delete(0, END)
                self.txtS_name.delete(0, END)
                self.txtM_name.delete(0, END)
                self.Position_combo.current(0)
                self.Department_combo.current(0)
                self.L_Center_combo.current(0)
                date.today()
                self.txtAge.delete(0, END)
                self.Gender_combo.current(0)
                self.txtRes_Adr.delete(0, END)
                self.txtCity.delete(0, END)
                self.Region_combo.current(0)
                self.txtCountry.delete(0, END)
                self.txtNationality.delete(0, END)
                self.M_Status_combo.current(0)
                self.Education_combo.current(0)
                self.txtMobile.delete(0, END)
                self.txtTelephone.delete(0, END)
                self.txtEmail.delete(0, END)
                self.txtOccupation.delete(0, END)
                null_photo()
                ChurchStatus.set("Active")
            except NameError:
                return None

        # for clear Display button
        def clearDisplay():
            display_result.delete('0.0', END)

        global paths
        paths = []  # required to save various file paths in a list to prevent using same image for the next user data

        # for add New button
        def addNew():
            if (len(Firstname.get()) and len(Surname.get()) and len(Department.get()) and len(
                    Mobile.get()) != 0):  # add last name and other important values before it allows saving to DB
                try:
                    if filename not in paths:
                        # print(filename)
                        byte_io = io.BytesIO()
                        my_photo_resized.save(byte_io, format='PNG')
                        byte_io = byte_io.getvalue()
                        Photo = byte_io
                        paths.append(filename)
                        # print(paths)
                    else:
                        # print('New filename received')
                        with open('Null_Image.jpg', 'rb') as newfile:
                            Photo = newfile.read()
                except NameError:
                    with open('Null_Image.jpg', 'rb') as newfile:
                        Photo = newfile.read()

                CGM_DB_BackEnd.addMemberRec(Prefix.get().upper(), Firstname.get().upper(), Surname.get().upper(),
                                            MiddleName.get().upper(), ChurchPosition.get().upper(),
                                            Department.get().upper(), LocalCenter.get().upper(), DoB.get(), Age.get(),
                                            Gender.get().upper(),
                                            Res_Address.get().upper(), City.get().upper(), Region.get().upper(),
                                            Country.get().upper(), Nationality.get().upper(),
                                            MaritalStatus.get().upper(), Education.get().upper(), Mobile.get(),
                                            Telephone.get(), Email.get(),
                                            Occupation.get().upper(), ChurchStatus.get().upper(), Photo)

                clearDisplay()
                result = '\nPrefix : {} \nFirst Name : {} \nSurname : {} \nMiddle Name : {} \nPosition : {} \nDepartment : {} ' \
                         '\nLocalCenter : {} \nDoB : {} \nAge : {} \nGender : {} \nAddress : {} \nCity : {} \nRegion : {}' \
                         ' \nCountry : {} \nNationality : {} \nMaritalStatus : {} \nEducation : {} \nMobile : {} \nTelephone : {}' \
                         ' \nEmail : {} \nOccupation : {} \nStatus : {}'.format(Prefix.get().upper(),
                                                                                Firstname.get().upper(),
                                                                                Surname.get().upper(),
                                                                                MiddleName.get().upper(),
                                                                                ChurchPosition.get().upper(),
                                                                                Department.get().upper(),
                                                                                LocalCenter.get().upper(), DoB.get(),
                                                                                Age.get(),
                                                                                Gender.get().upper(),
                                                                                Res_Address.get().upper(),
                                                                                City.get().upper(),
                                                                                Region.get().upper(),
                                                                                Country.get().upper(),
                                                                                Nationality.get().upper(),
                                                                                MaritalStatus.get().upper(),
                                                                                Education.get().upper(), Mobile.get(),
                                                                                Telephone.get(), Email.get(),
                                                                                Occupation.get().upper(),
                                                                                ChurchStatus.get().upper())

                display_result.insert(END, result)
                clearData()
                messagebox.showinfo("CGM Database Management System", "Submitted to Database", parent=root)
            else:
                messagebox.showinfo("CGM Database Management System", "Please fill all data !!!", parent=root)

        # pop up for Update function in Home Tab
        def edit_popup():
            Top = Toplevel(root)
            Top.title("CGM Database Management System")
            Top.geometry("700x500+1200+200")
            Top.configure(bg="gainsboro")
            Top.grab_set()  # avoids multiple instances of the toplevel window
            Top.resizable(0, 0)  # removes the maximize button

            def fetchID():
                for row in CGM_DB_BackEnd.searchID(ID.get()):
                    if str(row) == 'not found':
                        messagebox.showinfo("CGM Database Management System",
                                            "This Member ID doesn't exist in Records !!!", parent=Top)
                    else:
                        # print(row)
                        global var_ID  # useful for query of edit_profile function
                        var_ID = row[0]
                        lbl_nameTopValue.configure(text=row[2] + ' ' + row[4] + ' ' + row[3])
                        lbl_PositionTopValue.configure(text=row[5])
                        lbl_DepartmentTopValue.configure(text=row[6])
                        lbl_LocalCenterTopValue.configure(text=row[7])
                        it = row[23]
                        img = ImageTk.PhotoImage(data=it)
                        photo_labelTop.configure(image=img)
                        photo_labelTop.image = img

            def edit_profile():
                try:
                    for row in CGM_DB_BackEnd.searchID(var_ID):
                        self.Prefix_combo.set(row[1])
                        Firstname.set(row[2])
                        Surname.set(row[3])
                        MiddleName.set(row[4])
                        self.Position_combo.set(row[5])
                        self.Department_combo.set(row[6])
                        self.L_Center_combo.set(row[7])
                        DoB.set(row[8])
                        Age.set(row[9])
                        self.Gender_combo.set(row[10])
                        Res_Address.set(row[11])
                        City.set(row[12])
                        self.Region_combo.set(row[13])
                        Country.set(row[14])
                        Nationality.set(row[15])
                        self.M_Status_combo.set(row[16])
                        self.Education_combo.set(row[17])
                        Mobile.set(row[18])
                        Telephone.set((row[19]))
                        Email.set(row[20])
                        Occupation.set(row[21])
                        ChurchStatus.set(row[22])
                        global it  # required to recall (reuse of image) during update function
                        it = row[23]
                        img = ImageTk.PhotoImage(data=it)
                        photo_label.configure(image=img)
                        photo_label.image = img
                        Top.destroy()
                    # print(row)
                except NameError:
                    messagebox.showerror("CGM Database Management System", "No ID was fetched !!!", parent=Top)

            frame_EnterID = Frame(Top, padx=10, pady=10, bg="gainsboro", relief=RIDGE)
            frame_EnterID.grid(row=0, column=0)

            label_ID = Label(frame_EnterID, text="Enter member ID you wish to Edit: ", font=('arial', 12),
                             bg="gainsboro")
            label_ID.grid(row=0, column=0, padx=(10, 0), pady=10)

            ID = StringVar()
            entry_enterID = Entry(frame_EnterID, textvariable=ID, width=8, font=('arial', 15))
            entry_enterID.grid(row=0, column=1, padx=5, pady=10)

            button_fetch = Button(frame_EnterID, text="Fetch ID", font=('arial', 12, 'bold'), width=7,
                                  bd=4, bg='#03A9F4', command=fetchID, cursor='hand2')
            button_fetch.grid(row=0, column=2, padx=5, pady=10, sticky=E)

            bottom_frame = LabelFrame(Top, bd=1, padx=10, bg="gainsboro", relief=RIDGE, font=('arial', 13, 'bold'),
                                      text="Profile")
            bottom_frame.grid(row=1, column=0)

            frame_profile = Frame(bottom_frame, pady=10, bg="gainsboro", relief=RIDGE)  # padx=10,
            frame_profile.grid(row=0, column=0)

            # displays Null Image at profile area before ID input
            def displayPhoto():
                global photo_labelTop
                No_photoTop = ImageTk.PhotoImage(Image.open("Null_Image.jpg"))
                photo_labelTop = Label(frame_profile, image=No_photoTop)
                photo_labelTop.image = No_photoTop
                photo_labelTop.grid(row=0, column=0)

            displayPhoto()

            frame_details = Frame(bottom_frame, padx=5, pady=5, bg="gainsboro", relief=RIDGE)
            frame_details.grid(row=0, column=1)

            lbl_nameTop = Label(frame_details, text="Name :", bg="gainsboro")
            lbl_nameTop.grid(row=0, sticky=W, padx=5)

            lbl_PositionTop = Label(frame_details, text="Position :", bg="gainsboro")
            lbl_PositionTop.grid(row=1, sticky=W, padx=5)

            lbl_DepartmentTop = Label(frame_details, text="Department :", bg="gainsboro")
            lbl_DepartmentTop.grid(row=2, sticky=W, padx=5)

            lbl_LocalCenterTop = Label(frame_details, text="Local Center :", bg="gainsboro")
            lbl_LocalCenterTop.grid(row=3, sticky=W, padx=5)

            lbl_nameTopValue = Label(frame_details, text="", bg="gainsboro", width=40, anchor=W)
            lbl_nameTopValue.grid(row=0, column=1, sticky=E, padx=5)

            lbl_PositionTopValue = Label(frame_details, text="", bg="gainsboro", width=40, anchor=W)
            lbl_PositionTopValue.grid(row=1, column=1, sticky=E, padx=5)

            lbl_DepartmentTopValue = Label(frame_details, text="", bg="gainsboro", width=40, anchor=W)
            lbl_DepartmentTopValue.grid(row=2, column=1, sticky=E, padx=5)

            lbl_LocalCenterTopValue = Label(frame_details, text="", bg="gainsboro", width=40, anchor=W)
            lbl_LocalCenterTopValue.grid(row=3, column=1, sticky=E, padx=5)

            profile_button = Button(bottom_frame, text="Edit Profile", font=('arial', 12, 'bold'), height=1, width=11,
                                    bd=4, bg='#03A9F4', command=edit_profile, cursor='hand2')
            profile_button.grid(row=1, column=1, padx=10, pady=10, sticky=E)

        def Update():
            try:
                if var_ID == '':
                    messagebox.showerror("CGM Database Management System",
                                         "No member ID fetched !!!\nClue : Edit Data before you can update",
                                         parent=root)
                elif (len(Firstname.get()) and len(Surname.get()) and len(Department.get()) and len(Mobile.get()) != 0):

                    try:
                        if filename not in paths:
                            # print(filename)
                            byte_io = io.BytesIO()
                            my_photo_resized.save(byte_io, format='PNG')
                            byte_io = byte_io.getvalue()
                            Photo = byte_io
                            paths.append(filename)
                            # print(paths)
                        else:
                            Photo = it  # gets the photo (downloaded from DB) and resends to DB if no new photo is loaded
                    except NameError:
                        Photo = it  # gets the photo (downloaded from DB) and resends to DB if no new photo is loaded
                    """
                    try:
                        if filename:
                            byte_io = io.BytesIO()
                            my_photo_resized.save(byte_io, format='PNG')
                            byte_io = byte_io.getvalue()
                            Photo = byte_io

                    except NameError:
                        Photo = it  # gets the photo (downloaded from DB) and resends to DB if no new photo is loaded

                    """
                    CGM_DB_BackEnd.dataUpdate(var_ID, Prefix.get().upper(), Firstname.get().upper(),
                                              Surname.get().upper(), MiddleName.get().upper(),
                                              ChurchPosition.get().upper(),
                                              Department.get().upper(), LocalCenter.get().upper(), DoB.get(), Age.get(),
                                              Gender.get().upper(),
                                              Res_Address.get().upper(), City.get().upper(), Region.get().upper(),
                                              Country.get().upper(), Nationality.get().upper(),
                                              MaritalStatus.get().upper(), Education.get().upper(), Mobile.get(),
                                              Telephone.get(), Email.get(),
                                              Occupation.get().upper(), ChurchStatus.get().upper(), Photo)
                    clearDisplay()
                    result = '\nPrefix : {} \nFirst Name : {} \nSurname : {} \nMiddle Name : {} \nPosition : {} \nDepartment : {} ' \
                             '\nLocalCenter : {} \nDoB : {} \nAge : {} \nGender : {} \nAddress : {} \nCity : {} \nRegion : {}' \
                             ' \nCountry : {} \nNationality : {} \nMaritalStatus : {} \nEducation : {} \nMobile : {} \nTelephone : {}' \
                             ' \nEmail : {} \nOccupation : {} \nStatus : {}'.format(Prefix.get().upper(),
                                                                                    Firstname.get().upper(),
                                                                                    Surname.get().upper(),
                                                                                    MiddleName.get().upper(),
                                                                                    ChurchPosition.get().upper(),
                                                                                    Department.get().upper(),
                                                                                    LocalCenter.get().upper(),
                                                                                    DoB.get(), Age.get(),
                                                                                    Gender.get().upper(),
                                                                                    Res_Address.get().upper(),
                                                                                    City.get().upper(),
                                                                                    Region.get().upper(),
                                                                                    Country.get().upper(),
                                                                                    Nationality.get().upper(),
                                                                                    MaritalStatus.get().upper(),
                                                                                    Education.get().upper(),
                                                                                    Mobile.get(), Telephone.get(),
                                                                                    Email.get(),
                                                                                    Occupation.get().upper(),
                                                                                    ChurchStatus.get().upper())

                    display_result.insert(END, result)
                    clearData()
                    messagebox.showinfo("CGM Database Management System", "Update successful !", parent=root)

                else:
                    messagebox.showinfo("CGM Database Management System", "Please fill all data to Update !!!",
                                        parent=root)
            except NameError:
                messagebox.showerror("CGM Database Management System",
                                     "No member ID fetched !!!\nClue : Edit Data before you can update", parent=root)

        # FUNCTIONS FOR VIEW TAB
        # for View All button
        def veiw_all():
            delete_TreeviewItems()
            for row in CGM_DB_BackEnd.viewData():
                tree.insert("", END, values=row)  # tk.END if it doesn't work

        # deletes items in Tree view prior to pasting search result in
        def delete_TreeviewItems():
            TreeviewContents = tree.get_children()
            for item in TreeviewContents:
                dels = tree.delete(item)

        # for search button
        def search():
            delete_TreeviewItems()
            searchItem_selected = search_combo.get()

            Searched = searchItem.get().upper()

            def check():
                if str(row) == 'not found':
                    messagebox.showinfo("CGM Database Management System", "Searched Item doesn't exist in Records !!!",
                                        parent=root)
                else:
                    tree.insert("", END, values=row)

            if searchItem_selected == "Select Option":
                messagebox.showinfo("CGM Database Management System", "Please select Option to Search !!!", parent=root)

            elif Searched == '':
                messagebox.showinfo("CGM Database Management System", "No item typed in search box", parent=root)

            if searchItem_selected == "First Name":
                for row in CGM_DB_BackEnd.searchFirstname(Searched):
                    check()
            if searchItem_selected == "Last Name":
                for row in CGM_DB_BackEnd.searchSurname(Searched):
                    check()
            if searchItem_selected == "Middle Name":
                for row in CGM_DB_BackEnd.searchMiddlename(Searched):
                    check()
            if searchItem_selected == "Position":
                for row in CGM_DB_BackEnd.searchPosition(Searched):
                    check()
            if searchItem_selected == "Department":
                for row in CGM_DB_BackEnd.searchDepartment(Searched):
                    check()
            if searchItem_selected == "Local Center":
                for row in CGM_DB_BackEnd.searchLocalCenter(Searched):
                    check()
            if searchItem_selected == "Age":
                for row in CGM_DB_BackEnd.searchAge(Searched):
                    check()
            if searchItem_selected == "Gender":
                for row in CGM_DB_BackEnd.searchGender(Searched):
                    check()
            if searchItem_selected == "City":
                for row in CGM_DB_BackEnd.searchCity(Searched):
                    check()
            if searchItem_selected == "Region":
                for row in CGM_DB_BackEnd.searchRegion(Searched):
                    check()
            if searchItem_selected == "Country":
                for row in CGM_DB_BackEnd.searchCountry(Searched):
                    check()
            if searchItem_selected == "Nationality":
                for row in CGM_DB_BackEnd.searchNationality(Searched):
                    check()
            if searchItem_selected == "Education level":
                for row in CGM_DB_BackEnd.searchEducation(Searched):
                    check()
            if searchItem_selected == "Occupation":
                for row in CGM_DB_BackEnd.searchOccupation(Searched):
                    check()
            if searchItem_selected == "Status":
                for row in CGM_DB_BackEnd.searchChurchStatus(Searched):
                    check()

        def clearSearch():
            search_combo.current(0)
            entry_searchItem.delete(0, END)

        def clearResult():
            delete_TreeviewItems()

        def Delete():
            try:
                response = messagebox.askquestion("CGM Database Management System",
                                                  "Do you want to delete selected Record ?", parent=root)
                if response == "yes":
                    selected_item = tree.selection()[0]  # selection of the first item in Treeview row ie. the ID number
                    del_selected_item = tree.set(selected_item, '#1')
                    CGM_DB_BackEnd.deleteRec(del_selected_item)
                    tree.delete(tree.selection())
                    print (del_selected_item)
                else:
                    return None
            except IndexError:
                return None

        def export_as_csv():
            filename1 = str(txt_export.get())
            if filename1 != '':
                desktopDir = os.path.join((os.environ['USERPROFILE']), 'Desktop/')  # gets desktop directory  os.path.join(
                myfilename = desktopDir + filename1 + '.csv'
                with open(myfilename, 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerow(['ID', 'Prefix', 'First name', 'Surname', 'MiddleName', 'Position', 'Department',
                                     'LocalCenter', 'DoB', 'Age', 'Gender', 'Address', 'City', 'Region', 'Country',
                                     'Nationality', 'MaritalStatus', 'Education', 'Mobile', 'Telephone', 'Email',
                                     'Occupation', 'Status'])
                    for row_id in tree.get_children():
                        row1 = tree.item(row_id)['values'][:23]  # photo is omitted when exporting to csv file
                        print(row1)
                        writer.writerow(row1)
                    messagebox.showinfo("CGM Database Management System", '"File Exported As {} on to Desktop"'.format(filename1),
                                        parent=Top_export)
                    Top_export.destroy()
            else:
                messagebox.showinfo("CGM Database Management System", "Please enter the name you wish to save csv file",
                                    parent=Top_export)

        # pop up for Export function in View Tab
        def Export():
            # print(tree.get_children())
            if tree.get_children() != ():  # checks if there are characters in display area before export is possible
                global Top_export
                Top_export = Toplevel(root)
                Top_export.title("CGM Database Management System")
                Top_export.geometry("600x600+1200+200")
                Top_export.configure(bg="gainsboro")
                Top_export.grab_set()  # avoids multiple instances of the toplevel window
                Top_export.resizable(0, 0)  # removes the maximize button

                lbl_export = Label(Top_export, text="File name", padx=10, pady=10)
                lbl_export.grid(row=0, column=0)

                global txt_export
                txt_export = Entry(Top_export, font=('arial', 15), textvariable=Email, width=20)
                txt_export.grid(row=0, column=1, pady=5)

                Btn_exportCSV = Button(Top_export, text="To CSV", font=('arial', 12, 'bold'), height=1,
                                       width=9, bd=4, bg='#03A9F4', command=export_as_csv, cursor='hand2')
                Btn_exportCSV.grid(row=1, column=1)
            else:
                messagebox.showerror("CGM Database Management System",
                                     "Export is not possible.\n There is no display data to export!", parent=root)

        # ====================================== HOME TAB =============================================

        # ==============Home Tab Frames============
        DataFrame = Frame(home_tab, bd=1, padx=20, pady=20, relief=RIDGE, bg="Hotpink4", width=get_width*0.87, height=get_height*0.77)  # width=1200, height=700,
        DataFrame.grid(row=0, column=0)  # pack(fill=BOTH, expand=True)  # side=BOTTOM)

        DataFrameLEFT = LabelFrame(DataFrame, bd=1, padx=10, bg="Ghost white", relief=RIDGE,
                                   font=('arial', 20, 'bold'), text="Member Info\n", width=get_width*0.87, height=get_height*0.77)  # width=1000, height=700,
        DataFrameLEFT.grid(row=0, column=0, padx=10, pady=(0, 8)) #, sticky=W)
        for index in range(6):
            DataFrameLEFT.grid_columnconfigure(index, weight=1)
        DataFrameLEFT.grid_propagate(False)
        DataFrameLEFT.pack_propagate(False)

        DataFrameRIGHT = Frame(DataFrameLEFT, bd=1, padx=10, pady=5, bg="Ghost white",
                               relief=RIDGE)  # width=450, height=600,
        DataFrameRIGHT.grid(row=1, column=6, rowspan=7, padx=10, pady=10, sticky=E)

        # =========== Home Tab Labels and Entry Widget=============
        self.lblPrefix = Label(DataFrameLEFT, font=('arial', 15), text="Prefix:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblPrefix.grid(row=1, column=0, sticky=W)
        self.Prefix_combo = ttk.Combobox(DataFrameLEFT, textvariable=Prefix, state="readonly", font=('arial', 12),
                                         values=["Select Prefix", "Mr.", "Mrs.", "Miss.", "Dr.", "other"], width=23)
        self.Prefix_combo.grid(row=1, column=1)
        self.Prefix_combo.current(0)

        self.lblF_name = Label(DataFrameLEFT, font=('arial', 15), text="First name:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblF_name.grid(row=2, column=0, sticky=W)
        self.txtF_name = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Firstname, width=20, bd=2)
        self.txtF_name.grid(row=2, column=1, pady=5)

        self.lblS_name = Label(DataFrameLEFT, font=('arial', 15), text="Surname:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblS_name.grid(row=3, column=0, sticky=W)
        self.txtS_name = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Surname, width=20)
        self.txtS_name.grid(row=3, column=1, padx=20, pady=5)

        self.lblM_name = Label(DataFrameLEFT, font=('arial', 15), text="Middle name:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblM_name.grid(row=4, column=0, sticky=W)
        self.txtM_name = Entry(DataFrameLEFT, font=('arial', 15), textvariable=MiddleName, width=20)
        self.txtM_name.grid(row=4, column=1, pady=5)

        self.lblPosition = Label(DataFrameLEFT, font=('arial', 15), text="Position:", padx=2, pady=2,
                                 bg="Ghost White")
        self.lblPosition.grid(row=5, column=0, sticky=W)
        self.Position_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=ChurchPosition,
                                           values=Positions, font=('arial', 12), width=23)
        self.Position_combo.grid(row=5, column=1)
        self.Position_combo.current(0)

        self.lblDepartment = Label(DataFrameLEFT, font=('arial', 15), text="Department:", padx=2, pady=2,
                                   bg="Ghost White")
        self.lblDepartment.grid(row=6, column=0, sticky=W)
        self.Department_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=Department,
                                             values=Departments, font=('arial', 12), width=23)
        self.Department_combo.grid(row=6, column=1)
        self.Department_combo.current(0)

        self.lblL_Center = Label(DataFrameLEFT, font=('arial', 15), text="Local Center:", padx=2, pady=2,
                                 bg="Ghost White")
        self.lblL_Center.grid(row=7, column=0, sticky=W)
        self.L_Center_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=LocalCenter,
                                           values=LocalCenters, font=('arial', 12), width=23)
        self.L_Center_combo.grid(row=7, column=1)
        self.L_Center_combo.current(0)

        self.lblDoB = Label(DataFrameLEFT, font=('arial', 15), text="Date of Birth:", padx=2, pady=2,
                            bg="Ghost White")
        self.lblDoB.grid(row=1, column=2, sticky=W)
        today = date.today()
        cal = DateEntry(DataFrameLEFT, font=('arial', 12), width=23, textvariable=DoB, locale='en_US',
                        date_pattern='dd/mm/yyyy',
                        maxdate=today, background='darkblue', foreground='white', borderwidth=2)
        cal.grid(row=1, column=3, padx=10, pady=5)

        self.lblAge = Label(DataFrameLEFT, font=('arial', 15), text="Age:", padx=2, pady=2, bg="Ghost White")
        self.lblAge.grid(row=2, column=2, sticky=W)
        self.txtAge = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Age, width=20)
        self.txtAge.grid(row=2, column=3, pady=5)

        self.lblGender = Label(DataFrameLEFT, font=('arial', 15), text="Gender:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblGender.grid(row=3, column=2, sticky=W)
        self.Gender_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=Gender,
                                         values=["Select Gender", "Male", "Female"], font=('arial', 12), width=23)
        self.Gender_combo.grid(row=3, column=3)
        self.Gender_combo.current(0)

        self.lblRes_Adr = Label(DataFrameLEFT, font=('arial', 15), text="Res. Address:", padx=2, pady=2,
                                bg="Ghost White")
        self.lblRes_Adr.grid(row=4, column=2, sticky=W)
        self.txtRes_Adr = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Res_Address, width=20)
        self.txtRes_Adr.grid(row=4, column=3, pady=5)

        self.lblCity = Label(DataFrameLEFT, font=('arial', 15), text="City:", padx=2, pady=2, bg="Ghost White")
        self.lblCity.grid(row=5, column=2, sticky=W)
        self.txtCity = Entry(DataFrameLEFT, font=('arial', 15), textvariable=City, width=20)
        self.txtCity.grid(row=5, column=3, pady=5)

        self.lblRegion = Label(DataFrameLEFT, font=('arial', 15), text="Region:", padx=2, pady=2, bg="Ghost White")
        self.lblRegion.grid(row=6, column=2, sticky=W)
        self.Region_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=Region, value=Regions,
                                         font=('arial', 12), width=23)
        self.Region_combo.grid(row=6, column=3)
        self.Region_combo.current(0)

        self.lblCountry = Label(DataFrameLEFT, font=('arial', 15), text="Country:", padx=2, pady=2, bg="Ghost White")
        self.lblCountry.grid(row=7, column=2, sticky=W)
        self.txtCountry = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Country, width=20)
        self.txtCountry.grid(row=7, column=3, pady=5)

        self.lblNationality = Label(DataFrameLEFT, font=('arial', 15), text="Nationality:", padx=2, pady=2,
                                    bg="Ghost White")
        self.lblNationality.grid(row=1, column=4, sticky=W)
        self.txtNationality = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Nationality, width=20)
        self.txtNationality.grid(row=1, column=5, pady=5)

        self.lblM_Status = Label(DataFrameLEFT, font=('arial', 15), text="Marital Status:", padx=2, pady=2,
                                 bg="Ghost White")
        self.lblM_Status.grid(row=2, column=4, sticky=W)
        self.M_Status_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=MaritalStatus,
                                           font=('arial', 12),
                                           width=23, values=["Select Marital Status", "Married", "Single", "Widowed"])
        self.M_Status_combo.grid(row=2, column=5)
        self.M_Status_combo.current(0)

        self.lblEducation = Label(DataFrameLEFT, font=('arial', 15), text="Education", padx=2, pady=2, bg="Ghost White")
        self.lblEducation.grid(row=3, column=4, sticky=W)
        self.Education_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=Education,
                                            values=Education_levels, font=('arial', 12), width=23)
        self.Education_combo.grid(row=3, column=5)
        self.Education_combo.current(0)

        self.lblMobile = Label(DataFrameLEFT, font=('arial', 15), text="Mobile:", padx=2, pady=2, bg="Ghost White")
        self.lblMobile.grid(row=4, column=4, sticky=W)
        self.txtMobile = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Mobile, width=20)
        self.txtMobile.grid(row=4, column=5, pady=5)

        self.lblTelephone = Label(DataFrameLEFT, font=('arial', 15), text="Telephone:", padx=2, pady=2,
                                  bg="Ghost White")
        self.lblTelephone.grid(row=5, column=4, sticky=W)
        self.txtTelephone = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Telephone, width=20)
        self.txtTelephone.grid(row=5, column=5, pady=5)

        self.lblEmail = Label(DataFrameLEFT, font=('arial', 15), text="Email:", padx=2, pady=2, bg="Ghost White")
        self.lblEmail.grid(row=6, column=4, sticky=W)
        self.txtEmail = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Email, width=20)
        self.txtEmail.grid(row=6, column=5, pady=5)

        self.lblOccupation = Label(DataFrameLEFT, font=('arial', 15), text="Occupation:", padx=2, pady=2,
                                   bg="Ghost White")
        self.lblOccupation.grid(row=7, column=4, sticky=W)
        self.txtOccupation = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Occupation, width=20)
        self.txtOccupation.grid(row=7, column=5, pady=5)

        # Display Screen for newly added Data
        display_result = ScrolledText(DataFrameLEFT, height=5)
        display_result.grid(row=9, column=1, padx=5, pady=5, columnspan=7)  # ipadx=100
        display_result.bind("<FocusIn>", defocus)

        # Adds photo
        photo_frame = LabelFrame(DataFrameRIGHT, text="Photo", width=200, height=200, padx=5, pady=5, bg="ghost white")
        photo_frame.grid(row=0, column=0, pady=10)

        def null_photo():
            global photo_label
            No_photo = ImageTk.PhotoImage(Image.open("Null_Image.jpg"))
            photo_label = Label(photo_frame, image=No_photo)
            photo_label.image = No_photo
            photo_label.grid(row=0, column=0)

        def add_photo():
            try:
                global member_photo, filename, my_photo_resized
                filename = filedialog.askopenfilename(filetypes=(("JPG files", "*.jpg"), ("JPEG files", "*.jpeg"),
                                                                 ("PNG files", "*.png")))
                # filename2 = os.path.basename(filename)
                # vague_frame = Frame(photo_frame)
                my_photo = Image.open(filename)
                my_photo_resized = my_photo.resize((189, 220), Image.ANTIALIAS)
                member_photo = ImageTk.PhotoImage(my_photo_resized)
                photo_label.config(image=member_photo)
            except AttributeError:
                return None

        null_photo()  # displays "Null image" when program runs. ie. before file dialog is used to load image

        self.photo_button = Button(DataFrameRIGHT, text="Add Photo", bg='#03A9F4', command=add_photo, cursor='hand2')
        self.photo_button.grid(row=1, column=0)

        status_frame = LabelFrame(DataFrameRIGHT, text="Status", width=200, height=100, bg="ghost white")
        status_frame.grid(row=2, column=0, pady=10)

        # sets Active value for radio button
        ChurchStatus.set("Active")
        # Status radio buttons
        rad1 = Radiobutton(status_frame, text="Active", variable=ChurchStatus, value="Active", padx=40, pady=5,
                           bg="ghost white").pack(side=TOP)
        rad2 = Radiobutton(status_frame, text="Passive", variable=ChurchStatus, value="Passive", padx=40, pady=5,
                           bg="ghost white").pack(side=BOTTOM)

        # ============ Home Tab Buttons =====================

        self.btnClearEntry = Button(DataFrameLEFT, text="Clear Entry", font=('arial', 12, 'bold'), height=1, width=9,
                                    bd=4, bg='#03A9F4', command=clearData, cursor='hand2')
        self.btnClearEntry.grid(row=8, column=2, pady=15)

        self.btn_addNew = Button(DataFrameLEFT, text="Add New", font=('arial', 12, 'bold'), height=1, width=9, bd=4,
                                 bg='#03A9F4', command=addNew, cursor='hand2')
        self.btn_addNew.grid(row=8, column=3, pady=10)

        self.btn_Edit = Button(DataFrameLEFT, text="Edit Data", font=('arial', 12, 'bold'), height=1, width=9, bd=4,
                               bg='#03A9F4', command=edit_popup, cursor='hand2')
        self.btn_Edit.grid(row=8, column=4, pady=10)

        self.btn_Update = Button(DataFrameLEFT, text="Update", font=('arial', 12, 'bold'), height=1, width=10,
                                 bd=4, bg='#03A9F4', command=Update, cursor='hand2')
        self.btn_Update.grid(row=8, column=5, pady=10)

        self.btnClearDisplay = Button(DataFrameLEFT, text="Clear Display", font=('arial', 12, 'bold'), height=1,
                                      width=10,
                                      bd=4, bg='#03A9F4', command=clearDisplay, cursor='hand2')
        self.btnClearDisplay.grid(row=10, column=3, pady=15)

        # exit Button
        exit_image = ImageTk.PhotoImage(Image.open("Exit_icon.jpg"))
        self.btnExit = Button(my_notebook, image=exit_image, height=100, width=176, command=iExit, cursor='hand2')
        self.btnExit.image = exit_image
        self.btnExit.place(x=0, y=317)

        # ============================ VIEW TAB ============================================================

        # ===========View Tab Frames===============
        View_DataFrame = Frame(view_tab, bd=1, padx=20, pady=20, relief=RIDGE, bg="Hotpink4", width=get_width*0.87, height=get_height*0.77)
        View_DataFrame.grid(row=0, column=0)   # pack( fill=X, expand=True)

        View_DataFrameLEFT = Frame(View_DataFrame, bd=1, padx=10, bg="Ghost white", relief=RIDGE, width=get_width*0.87, height=get_height*0.77)
        View_DataFrameLEFT.grid(padx=10, pady=5)  # pack(fill=X, expand=True, padx=10)
        View_DataFrameLEFT.grid_columnconfigure(1, weight=1)
        View_DataFrameLEFT.grid_propagate(False)
        View_DataFrameLEFT.pack_propagate(False)

        View_DataFrameLEFT_Top = Frame(View_DataFrameLEFT, bg="Ghost white", relief=RIDGE)
        View_DataFrameLEFT_Top.grid(row=0, column=0, pady=15, ipadx=200)

        View_DataFrameLEFT_Bottom = Frame(View_DataFrameLEFT, bg="Ghost white", relief=RIDGE)
        View_DataFrameLEFT_Bottom.grid(row=1, column=0, ipadx=200)

        # ============View Tab Buttons==========

        label_searchBy = Label(View_DataFrameLEFT_Top, text="Search By", padx=5, pady=5, font=('Calibri', 13, 'bold'))
        label_searchBy.grid(row=0, column=0, pady=10)

        SearchOptions = ["Select Option", "First Name", "Last Name", "Middle Name", "Position", "Department",
                         "Local Center",
                         "Age", "Gender", "City", "Region", "Country", "Nationality", "Education level", "Occupation",
                         "Status"]
        search_combo = ttk.Combobox(View_DataFrameLEFT_Top, values=SearchOptions, state="readonly",
                                    font=('arial', 12), width=20)
        search_combo.grid(row=0, column=1, padx=10)
        search_combo.current(0)
        search_combo.bind("<FocusIn>", defocus)  # removes focus or highlighting

        searchItem = StringVar()
        entry_searchItem = Entry(View_DataFrameLEFT_Top, textvariable=searchItem, font=("Calibri", 12), width=40, bd=5)
        entry_searchItem.grid(row=0, column=2)

        button_search = Button(View_DataFrameLEFT_Top, text="Search", font=('arial', 12, 'bold'), height=1, width=9,
                               bd=4,
                               bg='#03A9F4', command=search, cursor='hand2')
        button_search.grid(row=0, column=3, padx=10, pady=10)

        button_clearSearch = Button(View_DataFrameLEFT_Top, text="Clear Search", font=('arial', 12, 'bold'), height=1,
                                    width=10, bd=4, bg='#03A9F4', command=clearSearch, cursor='hand2')
        button_clearSearch.grid(row=0, column=4, padx=10, pady=10)

        viewAll_button = Button(View_DataFrameLEFT_Top, text="View All", font=('arial', 12, 'bold'), height=1, width=9,
                                bd=4, bg='#03A9F4', command=veiw_all, cursor='hand2')
        viewAll_button.grid(row=1, column=0, padx=10, pady=5)

        button_clearResult = Button(View_DataFrameLEFT_Top, text="Clear Result", font=('arial', 12, 'bold'), height=1,
                                    width=10, bd=4, bg='#03A9F4', command=clearResult, cursor='hand2')
        button_clearResult.grid(row=1, column=1, padx=10, pady=10)

        button_Export = Button(View_DataFrameLEFT_Top, text="Export", font=('arial', 12, 'bold'), height=1,
                               width=9, bd=4, bg='forest green', command=Export, cursor='hand2')
        button_Export.grid(row=1, column=2, padx=10, pady=10)

        button_Delete = Button(View_DataFrameLEFT_Top, text="Delete", font=('arial', 12, 'bold'), height=1,
                               width=9, bd=4, bg='#03A9F4', command=Delete, cursor='hand2')
        button_Delete.grid(row=1, column=3, padx=10, pady=10)

        # TreeView
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 10, "bold"))
        columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

        tree = ttk.Treeview(View_DataFrameLEFT_Bottom, selectmode=BROWSE, column=columns, height=30, show='headings',
                            style="mystyle.Treeview")
        tree.grid(row=0, column=0)

        # Treeview headings
        tree.heading(1, text="ID", anchor=W)
        tree.heading(2, text="Prefix", anchor=W)
        tree.heading(3, text="First Name", anchor=W)
        tree.heading(4, text="Surname", anchor=W)
        tree.heading(5, text="Middle Name", anchor=W)
        tree.heading(6, text="Position", anchor=W)
        tree.heading(7, text="Department", anchor=W)
        tree.heading(8, text="Local Center", anchor=W)
        tree.heading(9, text="Date of Birth", anchor=W)
        tree.heading(10, text="Age", anchor=W)
        tree.heading(11, text="Gender", anchor=W)
        tree.heading(12, text="Address", anchor=W)
        tree.heading(13, text="City", anchor=W)
        tree.heading(14, text="Region", anchor=W)
        tree.heading(15, text="Country", anchor=W)
        tree.heading(16, text="Nationality", anchor=W)
        tree.heading(17, text="Marital", anchor=W)
        tree.heading(18, text="Education", anchor=W)
        tree.heading(19, text="Mobile", anchor=W)
        tree.heading(20, text="Tel", anchor=W)
        tree.heading(21, text="Occupation", anchor=W)
        tree.heading(22, text="Department", anchor=W)
        tree.heading(23, text="Status", anchor=W)

        # Tree view columns n sizes
        tree.column(1, width=50, minwidth=100, stretch=True)
        tree.column(2, width=70, minwidth=100, stretch=True)
        tree.column(3, width=70, minwidth=100, stretch=True)
        tree.column(4, width=70, minwidth=100, stretch=True)
        tree.column(5, width=70, minwidth=100, stretch=True)
        tree.column(6, width=70, minwidth=100, stretch=True)
        tree.column(7, width=70, minwidth=100, stretch=True)
        tree.column(8, width=70, minwidth=100, stretch=True)
        tree.column(9, width=70, minwidth=100, stretch=True)
        tree.column(10, width=70, minwidth=100, stretch=True)
        tree.column(11, width=70, minwidth=100, stretch=True)
        tree.column(12, width=70, minwidth=100, stretch=True)
        tree.column(13, width=70, minwidth=100, stretch=True)
        tree.column(14, width=70, minwidth=100, stretch=True)
        tree.column(15, width=70, minwidth=100, stretch=True)
        tree.column(16, width=70, minwidth=100, stretch=True)
        tree.column(17, width=70, minwidth=100, stretch=True)
        tree.column(18, width=70, minwidth=100, stretch=True)
        tree.column(19, width=70, minwidth=100, stretch=True)
        tree.column(20, width=70, minwidth=100, stretch=True)
        tree.column(21, width=70, minwidth=100, stretch=True)
        tree.column(22, width=70, minwidth=100, stretch=True)
        tree.column(23, width=70, minwidth=100, stretch=True)

        # Inserting Scrollbar
        scroll_vertical = ttk.Scrollbar(View_DataFrameLEFT_Bottom, orient="vertical", command=tree.yview)
        scroll_vertical.grid(row=0, column=1, ipady=200)  # (side=RIGHT, fill='y')

        scroll_horizontal = ttk.Scrollbar(View_DataFrameLEFT_Bottom, orient="horizontal", command=tree.xview)
        scroll_horizontal.grid(row=1, column=0, sticky=EW, padx=8, pady=(0, 8))  # (side=BOTTOM, fill='x')

        tree.configure(yscrollcommand=scroll_vertical.set, xscrollcommand=scroll_horizontal.set)

        # ================================= ATTENDANCE TAB ==================================================
        # Attendance page functions
        def ClearEntry_Att():
            date.today()
            txt_Males.delete(0, END)
            txt_Females.delete(0, END)
            txt_Children.delete(0, END)
            txt_TotalAttendance.delete(0, END)
            txt_NewConverts.delete(0, END)
            txt_NewMembers.delete(0, END)

        def Submit_Att():
            if (len(ServiceDate.get()) and len(Males.get()) and len(Females.get()) and len(Children.get())
                    and len(TotalAttendance.get()) and len(NewMembers.get()) and len(NewConverts.get()) != 0):
                # #### ADD IF STATEMENTS TO CHECK IF ANY ENTRY IS NOT A NUMBER / DIGIT   ######
                if Males.get().isnumeric() and Females.get().isnumeric() and Children.get().isnumeric() and \
                        TotalAttendance.get().isnumeric() and NewMembers.get().isnumeric() and NewConverts.get().isnumeric():

                    CGM_DB_Attendance_Backend.addAttendanceRec(ServiceDate.get(), Males.get(), Females.get(),
                                                               Children.get(),
                                                               TotalAttendance.get(), NewMembers.get(),
                                                               NewConverts.get())
                    dummy = ''
                    result2 = [dummy, ServiceDate.get(), Males.get(), Females.get(), Children.get(),
                               TotalAttendance.get(),
                               NewMembers.get(), NewConverts.get()]
                    delete_Treeview_AttItems()  # clears the tree view for new entry
                    tree_Att.insert("", END,
                                    values=result2)  # (result2[0]), (result2[1]), (result2[2]), (result2[3]), (result2[4]),(result2[5]), (result2[6]), (result2[7])))  #(row[1])
                    ClearEntry_Att()  # clears entries after data is sent to DB
                    messagebox.showinfo("CGM Database Management System", "Data added successfully !", parent=root)
                else:
                    messagebox.showerror("CGM Database Management System", "Please type in Numbers (Integers) only !",
                                         parent=root)
            else:
                messagebox.showerror("CGM Database Management System", "All entries need to be filled", parent=root)

        # deletes items in Tree view prior to pasting new entry result in
        def delete_Treeview_AttItems():
            TreeviewContents = tree_Att.get_children()
            for item in TreeviewContents:
                dels_Att = tree_Att.delete(item)

        def Edit_Att():
            try:
                edit_selected_item = tree_Att.selection()[
                    0]  # selection of the first item in Treeview row ie. the ID number
                global Attendance_ListNo
                Attendance_ListNo = tree_Att.set(edit_selected_item, '#1')
                for row in CGM_DB_Attendance_Backend.searchID(Attendance_ListNo):
                    ServiceDate.set(row[1])
                    Males.set(row[2])
                    Females.set(row[3])
                    Children.set(row[4])
                    TotalAttendance.set(row[5])
                    NewMembers.set(row[6])
                    NewConverts.set(row[7])
            except IndexError:
                messagebox.showerror("CGM Database Management System", "Select item in Attendance list before Edit !!!",
                                     parent=root)

        def Update_Att():
            try:
                if Attendance_ListNo == '':
                    messagebox.showerror("CGM Database Management System",
                                         "You can only Update after editing an existing data !!!", parent=root)
                elif (len(ServiceDate.get()) and len(Males.get()) and len(Females.get()) and len(Children.get())
                      and len(TotalAttendance.get()) and len(NewMembers.get()) and len(NewConverts.get()) != 0):
                    if Males.get().isnumeric() and Females.get().isnumeric() and Children.get().isnumeric() and \
                            TotalAttendance.get().isnumeric() and NewMembers.get().isnumeric() and NewConverts.get().isnumeric():

                        CGM_DB_Attendance_Backend.dataUpdate(Attendance_ListNo, ServiceDate.get(), Males.get(),
                                                             Females.get(), Children.get(), TotalAttendance.get(),
                                                             NewMembers.get(), NewConverts.get())
                        result2 = [Attendance_ListNo, ServiceDate.get(), Males.get(), Females.get(), Children.get(),
                                   TotalAttendance.get(),
                                   NewMembers.get(), NewConverts.get()]
                        delete_Treeview_AttItems()  # clears the tree view for new entry
                        tree_Att.insert("", END, values=result2)
                        ClearEntry_Att()  # clears entries after data is sent to DB
                        messagebox.showinfo("CGM Database Management System", "Update successful !", parent=root)
                    else:
                        messagebox.showerror("CGM Database Management System",
                                             "Please type in Numbers (Integers) only !", parent=root)
                else:
                    messagebox.showerror("CGM Database Management System", "All entries need to be filled", parent=root)
            except NameError:
                messagebox.showinfo("CGM Database Management System",
                                    "You can only Update after editing an existing data !!!", parent=root)

        def ShowList_Att():
            delete_Treeview_AttItems()
            for row in CGM_DB_Attendance_Backend.viewData():
                tree_Att.insert("", END,
                                values=row)  # (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7])))

        def BarChart_Att():
            row = CGM_DB_Attendance_Backend.getServiceDate()
            try:
                Top_Bar = Toplevel(root)
                Top_Bar.title("CGM Database Management System")
                Top_Bar.geometry("+80+80")  # 600x600
                Top_Bar.configure(bg="gainsboro")
                Top_Bar.grab_set()  # avoids multiple instances of the toplevel window
                Top_Bar.resizable(0, 0)  # removes the maximize button

                fig = plt.figure(figsize=(8, 8))  # sets size of plot area
                x_data = [dt.datetime.strptime(d, '%d/%m/%Y') for d, in CGM_DB_Attendance_Backend.getServiceDate()]
                y_data = [int(d) for d, in CGM_DB_Attendance_Backend.getTotalAttendance()]

                plt.bar(x_data, y_data)
                plt.xticks(x_data, rotation=45)
                date_format = mpl_dates.DateFormatter('%b %d, %Y')
                plt.gca().xaxis.set_major_formatter(date_format)  # formats x axis
                plt.xlabel('Date of Service', fontsize=15, color='red')
                plt.ylabel('Total Attendance', fontsize=15, color='red')
                plt.title('CGM Attendance', fontsize=20, color='red')
                plt.tight_layout()  # adds padding to plot

                # specify the window as master
                canvas = FigureCanvasTkAgg(fig, master=Top_Bar)
                plot_widget = canvas.get_tk_widget()

                plot_widget.grid(row=0, column=0)

                toolbarFrame = Frame(master=Top_Bar)
                toolbarFrame.grid(row=1, column=0)
                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            except ValueError:
                return None

        def LinearGraph_Att():
            try:
                Top_Line = Toplevel(root)
                Top_Line.title("CGM Database Management System")
                Top_Line.geometry("+80+80")  # 600x600
                Top_Line.configure(bg="gainsboro")
                Top_Line.grab_set()  # avoids multiple instances of the toplevel window
                Top_Line.resizable(0, 0)  # removes the maximize button

                fig = plt.figure(figsize=(8, 8))
                x_data = [dt.datetime.strptime(d, '%d/%m/%Y') for d, in CGM_DB_Attendance_Backend.getServiceDate()]
                y_data = [int(d) for d, in CGM_DB_Attendance_Backend.getTotalAttendance()]

                plt.plot_date(x_data, y_data, linestyle='solid')
                plt.xticks(x_data, rotation=45)

                date_format = mpl_dates.DateFormatter('%b %d, %Y')
                plt.gca().xaxis.set_major_formatter(date_format)
                plt.xlabel('Date of Service', fontsize=15, color='red')
                plt.ylabel('Total Attendance', fontsize=15, color='red')
                plt.title('CGM Attendance', fontsize=20, color='red')
                plt.tight_layout()  # adds padding to plot

                # specify the window as master
                canvas = FigureCanvasTkAgg(fig, master=Top_Line)
                plot_widget = canvas.get_tk_widget()

                plot_widget.grid(row=0, column=0)

                # for Navigation toolbar
                toolbarFrame = Frame(master=Top_Line)
                toolbarFrame.grid(row=1, column=0)
                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            except ValueError:
                return None

        # =================== frames for attendance page======================

        Attendance_MainFrame = Frame(attendance_tab, bd=1, padx=20, pady=20, relief=RIDGE, bg="Hotpink4", width=get_width*0.87, height=get_height*0.77)
        Attendance_MainFrame.grid()   # pack()  # side=BOTTOM)  width=1300, height=800,  expand=True, fill=BOTH,

        Attendance_DataFrame = LabelFrame(Attendance_MainFrame, bd=1, padx=10, pady=10, bg="Ghost white", relief=RIDGE,
                                          font=('arial', 20, 'bold'), text="Attendance\n", width=get_width*0.87, height=get_height*0.77)  # width=1000, height=800,
        Attendance_DataFrame.grid(row=0, column=0, padx=18, pady=5) #, sticky=W)  # , expand=True, fill=BOTH
        Attendance_DataFrame.grid_columnconfigure(1, weight=1)
        Attendance_DataFrame.grid_propagate(False)
        Attendance_DataFrame.pack_propagate(False)

        Attendance_DataFrame_Left = LabelFrame(Attendance_DataFrame, bd=1, padx=10, pady=10, bg="Ghost white",
                                               relief=RIDGE)  # width=1000, height=800,
        Attendance_DataFrame_Left.pack(side=LEFT, anchor=N, padx=(12, 0))  # fill=BOTH, expand=True,

        Attendance_DataFrame_Right = Frame(Attendance_DataFrame, bd=1, padx=10, pady=10, bg="Ghost white",
                                           relief=RIDGE)  # width=1000, height=800,
        Attendance_DataFrame_Right.pack(side=RIGHT, anchor=N)  # fill=BOTH, expand=True,

        Attendance_DataFrame_Right_T = Frame(Attendance_DataFrame_Right, padx=10, pady=10, bg="Ghost white",
                                             relief=RIDGE)  # width=1000, height=800,
        Attendance_DataFrame_Right_T.pack(side=TOP)  # fill=BOTH, expand=True,

        Attendance_DataFrame_Right_B = Frame(Attendance_DataFrame_Right, padx=10, pady=10, bg="Ghost white",
                                             relief=RIDGE)  # width=1000, height=800,
        Attendance_DataFrame_Right_B.pack(side=BOTTOM, pady=(10, 33))  # fill=BOTH, expand=True,

        # ==================================================
        # Text variables for Attendance Tab
        ServiceDate = StringVar()
        Males = StringVar()
        Females = StringVar()
        Children = StringVar()
        TotalAttendance = StringVar()
        NewMembers = StringVar()
        NewConverts = StringVar()

        # ===================Labels and Entries of Attendance page ============
        lbl_ServiceDate = Label(Attendance_DataFrame_Left, font=('arial', 13), text="Date of service:", padx=2, pady=2,
                                bg="Ghost White")
        lbl_ServiceDate.grid(row=0, column=0, padx=(10, 0), pady=20, sticky=W)
        today = date.today()
        S_date = DateEntry(Attendance_DataFrame_Left, font=('arial', 15), width=12, textvariable=ServiceDate,
                           locale='en_US',
                           date_pattern='dd/mm/yyyy', maxdate=today, background='darkblue', foreground='white',
                           borderwidth=2)
        S_date.grid(row=0, column=1, padx=10, pady=5)
        # S_date.bind("<FocusIn>", defocus)

        lbl_Males = Label(Attendance_DataFrame_Left, font=('arial', 13), text="No. of Males:", padx=2, pady=2,
                          bg="Ghost White")
        lbl_Males.grid(row=1, column=0, padx=(10, 0), pady=20, sticky=W)
        txt_Males = Entry(Attendance_DataFrame_Left, font=('arial', 15), textvariable=Males, width=14)
        txt_Males.grid(row=1, column=1, pady=5)

        lbl_Females = Label(Attendance_DataFrame_Left, font=('arial', 13), text="No. of Females:", padx=2, pady=2,
                            bg="Ghost White")
        lbl_Females.grid(row=2, column=0, padx=(10, 0), pady=20, sticky=W)
        txt_Females = Entry(Attendance_DataFrame_Left, font=('arial', 15), textvariable=Females, width=14)
        txt_Females.grid(row=2, column=1, pady=5)

        lbl_Children = Label(Attendance_DataFrame_Left, font=('arial', 13), text="No. of Children:", padx=2, pady=2,
                             bg="Ghost White")
        lbl_Children.grid(row=3, column=0, padx=(10, 0), pady=20, sticky=W)
        txt_Children = Entry(Attendance_DataFrame_Left, font=('arial', 15), textvariable=Children, width=14)
        txt_Children.grid(row=3, column=1, pady=5)

        lbl_TotalAttendance = Label(Attendance_DataFrame_Left, font=('arial', 13), text="Total Attendance:", padx=2,
                                    pady=2,
                                    bg="Ghost White")
        lbl_TotalAttendance.grid(row=4, column=0, padx=(10, 0), pady=20, sticky=W)
        txt_TotalAttendance = Entry(Attendance_DataFrame_Left, font=('arial', 15), textvariable=TotalAttendance,
                                    width=14)
        txt_TotalAttendance.grid(row=4, column=1, pady=5)

        lbl_NewMembers = Label(Attendance_DataFrame_Left, font=('arial', 13), text="No. of New Members:", padx=2,
                               pady=2,
                               bg="Ghost White")
        lbl_NewMembers.grid(row=0, column=2, padx=(20, 0), pady=20, sticky=W)
        txt_NewMembers = Entry(Attendance_DataFrame_Left, font=('arial', 15), textvariable=NewMembers, width=14)
        txt_NewMembers.grid(row=0, column=3, padx=20, pady=5)

        lbl_NewConverts = Label(Attendance_DataFrame_Left, font=('arial', 13), text="No. of New Converts:", padx=2,
                                pady=2,
                                bg="Ghost White")
        lbl_NewConverts.grid(row=1, column=2, padx=(20, 0), pady=20, sticky=W)
        txt_NewConverts = Entry(Attendance_DataFrame_Left, font=('arial', 15), textvariable=NewConverts, width=14)
        txt_NewConverts.grid(row=1, column=3, padx=20, pady=5)

        # =============== Attendance page Buttons ======================
        # left frame buttons
        btnClearEntry_Att = Button(Attendance_DataFrame_Left, text="Clear Entry", font=('arial', 12, 'bold'), height=1,
                                   width=9,
                                   bd=4, bg='#03A9F4', command=ClearEntry_Att, cursor='hand2')
        btnClearEntry_Att.grid(row=6, column=0, pady=50)

        btnSubmit_Att = Button(Attendance_DataFrame_Left, text="Submit", font=('arial', 12, 'bold'), height=1, width=9,
                               bd=4, bg='#03A9F4', command=Submit_Att, cursor='hand2')
        btnSubmit_Att.grid(row=6, column=1, pady=50)

        btnEdit_Att = Button(Attendance_DataFrame_Left, text="Edit", font=('arial', 12, 'bold'), height=1, width=9,
                             bd=4, bg='#03A9F4', command=Edit_Att, cursor='hand2')
        btnEdit_Att.grid(row=6, column=2, pady=50)

        btnUpdate_Att = Button(Attendance_DataFrame_Left, text="Update", font=('arial', 12, 'bold'), height=1, width=9,
                               bd=4, bg='#03A9F4', command=Update_Att, cursor='hand2')
        btnUpdate_Att.grid(row=6, column=3, pady=50)

        # Right frame buttons

        btnShowList_Att = Button(Attendance_DataFrame_Right_B, text="Show Attendance List", font=('arial', 12, 'bold'),
                                 height=2, width=13,
                                 bd=4, bg='#03A9F4', wraplength=150, command=ShowList_Att, cursor='hand2')
        btnShowList_Att.grid(row=0, column=0, padx=(80, 30), pady=5)

        btnBarChart_Att = Button(Attendance_DataFrame_Right_B, text="Show Bar Chart", font=('arial', 12, 'bold'),
                                 height=2, width=10,
                                 bd=4, bg='#03A9F4', wraplength=120, command=BarChart_Att, cursor='hand2')
        btnBarChart_Att.grid(row=0, column=1, padx=30, pady=5)

        btnLinearGraph_Att = Button(Attendance_DataFrame_Right_B, text="Show Linear Graph", font=('arial', 12, 'bold'),
                                    height=2, width=10, bd=4, bg='#03A9F4', wraplength=150, command=LinearGraph_Att,
                                    cursor='hand2')
        btnLinearGraph_Att.grid(row=0, column=2, padx=30, pady=5)

        # Treeview for Attendance page
        columns_2 = [1, 2, 3, 4, 5, 6, 7, 8]

        tree_Att = ttk.Treeview(Attendance_DataFrame_Right_T, selectmode=BROWSE, column=columns_2, height=25,
                                show='headings', style="mystyle.Treeview")
        tree_Att.grid(row=0, column=0)

        # Treeview headings
        tree_Att.heading(1, text="No.", anchor=W)
        tree_Att.heading(2, text="Date", anchor=W)
        tree_Att.heading(3, text="Males", anchor=W)
        tree_Att.heading(4, text="Females", anchor=W)
        tree_Att.heading(5, text="Children", anchor=W)
        tree_Att.heading(6, text="Total", anchor=W)
        tree_Att.heading(7, text="New Members", anchor=W)
        tree_Att.heading(8, text="New Converts", anchor=W)

        # Tree view columns n sizes
        tree_Att.column(1, width=60, minwidth=40, stretch=True)
        tree_Att.column(2, width=70, minwidth=100, stretch=True)
        tree_Att.column(3, width=60, minwidth=80, stretch=True)
        tree_Att.column(4, width=60, minwidth=80, stretch=True)
        tree_Att.column(5, width=100, minwidth=80, stretch=True)
        tree_Att.column(6, width=100, minwidth=70, stretch=True)
        tree_Att.column(7, width=100, minwidth=116, stretch=True)
        tree_Att.column(8, width=100, minwidth=116, stretch=True)

        # Inserting Scrollbar
        scroll_vertical = ttk.Scrollbar(Attendance_DataFrame_Right_T, orient="vertical", command=tree_Att.yview)
        scroll_vertical.grid(row=0, column=1, ipady=200)  # (side=RIGHT, fill='y')

        scroll_horizontal = ttk.Scrollbar(Attendance_DataFrame_Right_T, orient="horizontal", command=tree_Att.xview)
        scroll_horizontal.grid(row=1, column=0, sticky=EW, padx=8, pady=(0, 8))  # (side=BOTTOM, fill='x')

        tree_Att.configure(yscrollcommand=scroll_vertical.set, xscrollcommand=scroll_horizontal.set)


if __name__ == '__main__':
    main()
