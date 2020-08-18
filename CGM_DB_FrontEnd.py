"""
Lines of codes to edit for various branches {necessary for unique ID on firebase}:
in "Sync_DataOnline()":
Search for all 'Tadi' and replace with 'Kum' (for Kumasi), 'Acc' (for Accra), 'Wamfie' (for Wamfie), ... etc
"""


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
import pyrebase
import requests  # for connection error
import base64


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

        lbl_background = Label(self.frame, image=self.bg_icon).pack()

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
        self.btnLogout.grid_columnconfigure(2, weight=1)  # New addition, to keep logout btn at the extreme left

        # ==========Notebook / Tabs============
        style = ttk.Style(self.root)
        style.configure("lefttab.TNotebook.Tab", padding=[40, 40], font=('arial', 11))
        style.configure("lefttab.TNotebook", tabposition='wn')

        """
        style.map("lefttab.TNotebook.Tab", foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'yellow'), ('active', 'orange')])
        """

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
        Regions = ["Select Region", "Ahafo", "Ashanti", "Bono-East", "Brong Ahafo", "Central",
                   "Eastern", "Greater Accra", "North East", "Northern", "Oti", "Savannah", "Upper East",
                   "Upper West", "Volta", "Western", "Western-North", "N/A"]

        Positions = ["Select Position", "Apostle", "Reverend", "Minister", "Elder", "Deacon",
                     "Lady Deacon", "Shepherd", "Ass. Shepherd", "member"]

        Departments = ["Select Department", "Blessed Choir", "Technical", "Ushering",
                       "Protocol", "Hospitality", "Children's Dept", "N/A"]

        LocalCenters = ["Select Local Center", "Anaji", "Apollo", "Assakae",
                        "Bakaekyir", "Kweikuma", "Kwesimintsim - main", "Kwesiminstim - zongo", "Lagos town", "Mempeasem",
                        "Mpintsin", "Sekondi", "Takoradi - Harbor", "Takoradi - number 2", "Accra", "Kumasi", "Wemfie", "N/A"]

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
        def Sync_DataOnline():
            try:
                config_list = []
                # Configuration for firebase

                config = {

                }

                firebase = pyrebase.initialize_app(config)
                #storage = firebase.storage()  # [: if request.auth != null]...to be added to read and write rules in firebase storage

                # Syncs member Database
                memberDB = firebase.database()
                memberDatabase = "memberDatabase"

                try:
                    # (Using realtime database)... Converts sqlite dB to NoSql on firebase dB
                    overall_IDs = []
                    paths = memberDB.child(memberDatabase).get()
                    for path in paths.each():
                        # print(path.key())
                        overall_IDs.append(path.key())  # gets over all list of overall_IDs
                        # print(path.val())

                    #print(overall_IDs)
                    branch_IDs = [i for i in overall_IDs if
                                  i.startswith('Tadi')]  # picks only ID's of specific church branch
                    #print(branch_IDs)

                    local_IDs = []
                    for row in CGM_DB_BackEnd.viewData():
                        ID = "Tadi" + str(row[0])  # change ID's for kumasi:Kum, Accra:Acc, etc
                        Has_synced = row[24]

                        """
                        Photo_encoded = row[23]
                        print(Photo_encoded)
                        Photo = Photo_encoded.decode('utf-8')
                        
                        #print(Photo)
                        """
                        local_IDs.append(ID)
                        # print('Local ID list is:{}'.format(local_IDs))
                        if ID in branch_IDs:
                            if Has_synced == 'false':  # Data has been synced before but has been updated in local dB again
                                data = {
                                    "Prefix": row[1], "First name": row[2], "Last name": row[3], "Middle name": row[4],
                                    "Position": row[5], "Department": row[6], "Local Center": row[7], "DoB": row[8],
                                    "Age": row[9],
                                    "Gender": row[10], "Address": row[11], "City": row[12], "Region": row[13],
                                    "Country": row[14],
                                    "Nationality": row[15], "Marital": row[16], "Education": row[17], "Mobile": row[18],
                                    "Telephone": row[19], "Email": row[20], "Occupation": row[21],
                                    "Status": row[22]}  #, "Photo": Photo}
                                memberDB.child(memberDatabase).child(ID).set(data)
                                Has_synced_updated = 'true'
                                CGM_DB_BackEnd.dataUpdate(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                                          row[7], row[8],
                                                          row[9], row[10], row[11], row[12], row[13], row[14], row[15],
                                                          row[16], row[17], row[18], row[19],
                                                          row[20], row[21], row[22], row[23], Has_synced_updated)
                        else:  # New Data that has not been synced before
                            """
                            Photo_encoded = row[23]
                            Photo = Photo_encoded.decode('utf-8')
                            """
                            data = {
                                "Prefix": row[1], "First name": row[2], "Last name": row[3], "Middle name": row[4],
                                "Position": row[5], "Department": row[6], "Local Center": row[7], "DoB": row[8],
                                "Age": row[9],
                                "Gender": row[10], "Address": row[11], "City": row[12], "Region": row[13],
                                "Country": row[14],
                                "Nationality": row[15], "Marital": row[16], "Education": row[17], "Mobile": row[18],
                                "Telephone": row[19], "Email": row[20], "Occupation": row[21],
                                "Status": row[22]}  # , "Photo": Photo}

                            memberDB.child(memberDatabase).child(ID).set(data)
                            Has_synced_updated = 'true'
                            CGM_DB_BackEnd.dataUpdate(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                      row[8],
                                                      row[9], row[10], row[11], row[12], row[13], row[14], row[15],
                                                      row[16], row[17], row[18], row[19],
                                                      row[20], row[21], row[22], row[23], Has_synced_updated) # Updates local dB if data syncs online
                    # print('Local ID list is:{}'.format(local_IDs))
                    """  # Delete function is commented out to avoid total deletion of all data from firebase when a 
                         # user re-installs app for any reason(ie. with new local dB data)
                    for item in branch_IDs:
                        if item not in local_IDs:
                            memberDB.child(memberDatabase).child(item).remove()
                    """
                except TypeError:  # TypeError will be returned during first time syncing when 'branch_IDs' returns none. Hence needed for first time sync
                    for row in CGM_DB_BackEnd.viewData():
                        ID = "Tadi" + str(row[0])
                        # Has_synced = row[24] # Has_synced will be false already before first sync
                        """
                        Photo_encoded = row[23]
                        Photo = Photo_encoded.decode('utf-8')
                        """

                        data = {
                            "Prefix": row[1], "First name": row[2], "Last name": row[3], "Middle name": row[4],
                            "Position": row[5], "Department": row[6], "Local Center": row[7], "DoB": row[8],
                            "Age": row[9],
                            "Gender": row[10], "Address": row[11], "City": row[12], "Region": row[13],
                            "Country": row[14],
                            "Nationality": row[15], "Marital": row[16], "Education": row[17], "Mobile": row[18],
                            "Telephone": row[19], "Email": row[20], "Occupation": row[21],
                            "Status": row[22]}  # , "Photo": Photo}
                        memberDB.child(memberDatabase).child(ID).set(data)
                        Has_synced_updated = 'true'
                        CGM_DB_BackEnd.dataUpdate(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                  row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15],
                                                  row[16], row[17], row[18], row[19],
                                                  row[20], row[21], row[22], row[23], Has_synced_updated)

                """
                # (Using cloud Storage)... Syncs local dB to cloud by uploading whole local file
                path_on_cloud = "memberDatabase/memberCGM.db"
                path_local = "memberCGM.db"
                storage.child(path_on_cloud).put(path_local)  # uploads attendance DB file to firebase storage
                # storage.child(path2_on_cloud).download("attendanceCGM.db")  # downloads attendance DB file from firebase to local
                """

                # Syncs Attendance Database
                attendanceDB = firebase.database()
                attendanceDatabase = "attendanceDatabase"

                try:
                    # (Using realtime database)... Converts sqlite dB to NoSql on firebase dB
                    overall_IDsAtt = []
                    paths = attendanceDB.child(attendanceDatabase).get()
                    for path in paths.each():
                        #print(path.key())
                        overall_IDsAtt.append(path.key())   # gets over all list of overall_IDs
                        #print(path.val())

                    #print(overall_IDsAtt)
                    branch_IDsAtt = [i for i in overall_IDsAtt if i.startswith('Tadi')]  # picks only ID's of specific church branch
                    #print(branch_IDsAtt)

                    local_IDsAtt = []
                    for row in CGM_DB_Attendance_Backend.viewData():
                        IDAtt = "Tadi" + str(row[0])  # change IDAtt for kumasi:Kum, Accra:Acc, etc
                        Has_synced = row[8]

                        local_IDsAtt.append(IDAtt)
                        #print('Local IDAtt list is:{}'.format(local_IDs))
                        if IDAtt in branch_IDsAtt:
                            if Has_synced == 'false':  # Data has been synced before but has been updated in local dB again
                                data = {
                                    "1 Date": row[1],
                                    "2 Males": row[2],
                                    "3 Females": row[3],
                                    "4 Children": row[4],
                                    "5 Total": row[5],
                                    "6 New members": row[6],
                                    "7 New converts": row[7]
                                }
                                attendanceDB.child(attendanceDatabase).child(IDAtt).set(data)
                                Has_synced_updated = 'true'
                                CGM_DB_Attendance_Backend.dataUpdate(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], Has_synced_updated)
                        else:  # New Data that has not been synced before
                            data = {
                                "1 Date": row[1],
                                "2 Males": row[2],
                                "3 Females": row[3],
                                "4 Children": row[4],
                                "5 Total": row[5],
                                "6 New members": row[6],
                                "7 New converts": row[7]
                            }
                            attendanceDB.child(attendanceDatabase).child(IDAtt).set(data)
                            Has_synced_updated = 'true'
                            CGM_DB_Attendance_Backend.dataUpdate(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                                                 row[7], Has_synced_updated)
                            #print('Local IDAtt list is:{}'.format(local_IDs))
                    """
                    # commented out because no delete function required in Attendance DB
                    for item in branch_IDsAtt:
                        if item not in local_IDsAtt:
                            attendanceDB.child(attendanceDatabase).child(item).remove()
                    """
                except TypeError:   # TypeError will be returned during first time syncing when 'branch_IDs' returns none. Hence needed for first time sync
                    for row in CGM_DB_Attendance_Backend.viewData():
                        IDAtt = "Tadi" + str(row[0])  # change IDAtt for kumasi:Kum, Accra:Acc, etc
                        #Has_synced = row[24] # Has_synced will be false already before first sync
                        data = {
                            "1 Date": row[1],
                            "2 Males": row[2],
                            "3 Females": row[3],
                            "4 Children": row[4],
                            "5 Total": row[5],
                            "6 New members": row[6],
                            "7 New converts": row[7]
                        }
                        attendanceDB.child(attendanceDatabase).child(IDAtt).set(data)
                        Has_synced_updated = 'true'
                        CGM_DB_Attendance_Backend.dataUpdate(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                                             row[7], Has_synced_updated)
                """
                # (Using cloud Storage)... Syncs local dB to cloud by uploading whole local file
                path2_on_cloud = "attendanceDatabase/attendanceCGM.db"
                path2_local = "attendanceCGM.db"
                storage.child(path2_on_cloud).put(path2_local)  # uploads attendance DB file to firebase storage
                # storage.child(path2_on_cloud).download("attendanceCGM.db")  # downloads attendance DB file from firebase to local
                """

            except requests.exceptions.ConnectionError:
                messagebox.showerror("CGM Database Management System", "Data cannot be synced.\nPlease check your internet connection and Try again.", parent=root)



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

        # for add New function to be called in Save function
        def addNew():
            if (len(Firstname.get()) and len(Surname.get()) and len(Department.get()) and len(
                    Mobile.get()) != 0):  # add last name and other important values before it allows saving to DB
                try:
                    if filename not in paths:
                        print(filename)
                        byte_io = io.BytesIO()
                        my_photo_resized.save(byte_io, format='PNG')
                        byte_io = byte_io.getvalue()
                        Photo_decode = byte_io  # gets io byte string from image file
                        paths.append(filename)
                        Photo = base64.b64encode(Photo_decode)  # converts io string into base64 byte string
                        #print(Photo)
                        #new = Photo.decode('utf-8')
                        #print('new one is:'+ new)
                        # print(paths)
                    else:
                        # print('New filename received')
                        null_photo = Image.open('Null_Image.jpg')
                        byte_io = io.BytesIO()
                        null_photo.save(byte_io, format='PNG')
                        byte_io = byte_io.getvalue()
                        Photo_decode = byte_io  # gets io byte string from image file
                        Photo = base64.b64encode(Photo_decode)
                        #with open('Null_Image.jpg', 'rb') as newfile:
                         #   Photo = base64.b64encode(newfile.read())

                except NameError:
                    null_photo = Image.open('Null_Image.jpg')
                    byte_io = io.BytesIO()
                    null_photo.save(byte_io, format='PNG')
                    byte_io = byte_io.getvalue()
                    Photo_decode = byte_io  # gets io byte string from image file
                    Photo = base64.b64encode(Photo_decode)
                    #with open('Null_Image.jpg', 'rb') as newfile:
                     #   Photo = base64.b64encode(newfile.read())
                Has_synced = 'false'
                CGM_DB_BackEnd.addMemberRec(Prefix.get().upper(), Firstname.get().upper(), Surname.get().upper(),
                                            MiddleName.get().upper(), ChurchPosition.get().upper(),
                                            Department.get().upper(), LocalCenter.get().upper(), DoB.get(), Age.get(),
                                            Gender.get().upper(),
                                            Res_Address.get().upper(), City.get().upper(), Region.get().upper(),
                                            Country.get().upper(), Nationality.get().upper(),
                                            MaritalStatus.get().upper(), Education.get().upper(), Mobile.get(),
                                            Telephone.get(), Email.get(),
                                            Occupation.get().upper(), ChurchStatus.get().upper(), Photo, Has_synced)

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
                messagebox.showinfo("CGM Database Management System", "Submitted successfully to Database", parent=root)
            else:
                messagebox.showinfo("CGM Database Management System", "Please fill all required data !!!\n(Name, Position, Department, Local center, Mobile)", parent=root)


        def Update():
            try:
                if var_ID == '':
                    messagebox.showerror("CGM Database Management System",
                                         "No member ID fetched !!!\nClue : Edit Data before you can update",
                                         parent=root)
                elif (len(Firstname.get()) and len(Surname.get()) and len(Department.get()) and len(Mobile.get()) != 0):

                    try:
                        if filename not in paths:
                            print(filename)
                            byte_io = io.BytesIO()
                            my_photo_resized.save(byte_io, format='PNG')
                            byte_io = byte_io.getvalue()
                            Photo_decode = byte_io
                            #paths.append(filename)
                            Photo = base64.b64encode(Photo_decode)
                            #print(Photo)
                        else:
                            Photo = it  # gets the photo (downloaded from DB) and resends to DB if no new photo is loaded
                    except NameError:
                        Photo = it  # gets the photo (downloaded from DB) and resends to DB if no new photo is loaded
                    Has_synced = 'false'
                    CGM_DB_BackEnd.dataUpdate(var_ID, Prefix.get().upper(), Firstname.get().upper(),
                                              Surname.get().upper(), MiddleName.get().upper(),
                                              ChurchPosition.get().upper(),
                                              Department.get().upper(), LocalCenter.get().upper(), DoB.get(), Age.get(),
                                              Gender.get().upper(),
                                              Res_Address.get().upper(), City.get().upper(), Region.get().upper(),
                                              Country.get().upper(), Nationality.get().upper(),
                                              MaritalStatus.get().upper(), Education.get().upper(), Mobile.get(),
                                              Telephone.get(), Email.get(),
                                              Occupation.get().upper(), ChurchStatus.get().upper(), Photo, Has_synced)
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
                    messagebox.showinfo("CGM Database Management System", "Please fill all required data to Update !!!",
                                        parent=root)
            except NameError:
                messagebox.showerror("CGM Database Management System",
                                     "You can only Update after Editing Profile", parent=root)


        # FUNCTIONS FOR VIEW TAB
        # for View All button
        def veiw_all():
            delete_TreeviewItems()
            for row in CGM_DB_BackEnd.viewData():
                #print(row)  # to be deleted later
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

        def clearDisplay2():
            delete_TreeviewItems()
            displayPhoto()
            lbl_nameTopValue.configure(text='')
            lbl_PositionTopValue.configure(text='')
            lbl_DepartmentTopValue.configure(text='')
            lbl_LocalCenterTopValue.configure(text='')
            lbl_AddressTopValue.configure(text='')
            lbl_cityTopValue.configure(text='')
            lbl_NationalityTopValue.configure(text='')
            lbl_mobileTopValue.configure(text='')
            lbl_statusTopValue.configure(text='')

        def Delete():
            try:
                response = messagebox.askquestion("CGM Database Management System",
                                                  "Do you want to delete selected Record ?", parent=root)
                if response == "yes":
                    selected_item = tree.selection()[0]  # selection of the first item in Treeview row ie. the ID number
                    del_selected_item = tree.set(selected_item, '#1')
                    CGM_DB_BackEnd.deleteRec(del_selected_item)
                    tree.delete(tree.selection())
                    #print (del_selected_item)
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
                                     'Occupation', 'Status'])  # 'Photo'
                    for row_id in tree.get_children():
                        row1 = tree.item(row_id)['values'][:23]  # photo is omitted when exporting to csv file...NB>Photo added for now for check
                        #print(row1)
                        writer.writerow(row1)
                    messagebox.showinfo("CGM Database Management System", '"File Exported As {} on to Desktop"'.format(filename1),
                                        parent=Top_export)
                    Top_export.destroy()
            else:
                messagebox.showinfo("CGM Database Management System", "Please enter the name you wish to save excel file",
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

                Btn_exportCSV = Button(Top_export, text="To Excel", font=('arial', 12, 'bold'), height=1,
                                       width=9, bd=4, bg='turquoise1', command=export_as_csv, cursor='hand2')
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
        DataFrameLEFT.grid(row=0, column=0, padx=18, pady=(0, 8)) #, sticky=W)
        for index in range(6):
            DataFrameLEFT.grid_columnconfigure(index, weight=1)  # spaces columns well
        DataFrameLEFT.grid_propagate(False)
        DataFrameLEFT.pack_propagate(False)

        DataFrameRIGHT = Frame(DataFrameLEFT, bd=1, padx=10, pady=5, bg="Ghost white",
                               relief=RIDGE)  # width=450, height=600,
        DataFrameRIGHT.grid(row=1, column=6, rowspan=7, padx=10, pady=10, sticky=E)

        # =========== Home Tab Labels and Entry Widget=============
        self.lblPrefix = Label(DataFrameLEFT, font=('arial', 15), text="Prefix:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblPrefix.grid(row=1, column=0, padx=10, sticky=W)
        self.Prefix_combo = ttk.Combobox(DataFrameLEFT, textvariable=Prefix, state="readonly", font=('arial', 12),
                                         values=["Select Prefix", "Mr.", "Mrs.", "Miss.", "Dr.", "other"], width=23)
        self.Prefix_combo.grid(row=1, column=1)
        self.Prefix_combo.current(0)

        self.lblF_name = Label(DataFrameLEFT, font=('arial', 15), text="First name:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblF_name.grid(row=2, column=0, padx=10, sticky=W)
        self.txtF_name = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Firstname, width=20, bd=2)
        self.txtF_name.grid(row=2, column=1, pady=5)

        self.lblS_name = Label(DataFrameLEFT, font=('arial', 15), text="Surname:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblS_name.grid(row=3, column=0, padx=10, sticky=W)
        self.txtS_name = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Surname, width=20)
        self.txtS_name.grid(row=3, column=1, padx=20, pady=5)

        self.lblM_name = Label(DataFrameLEFT, font=('arial', 15), text="Middle name:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblM_name.grid(row=4, column=0, padx=10, sticky=W)
        self.txtM_name = Entry(DataFrameLEFT, font=('arial', 15), textvariable=MiddleName, width=20)
        self.txtM_name.grid(row=4, column=1, pady=5)

        self.lblPosition = Label(DataFrameLEFT, font=('arial', 15), text="Position:", padx=2, pady=2,
                                 bg="Ghost White")
        self.lblPosition.grid(row=5, column=0, padx=10, sticky=W)
        self.Position_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=ChurchPosition,
                                           values=Positions, font=('arial', 12), width=23)
        self.Position_combo.grid(row=5, column=1)
        self.Position_combo.current(0)

        self.lblDepartment = Label(DataFrameLEFT, font=('arial', 15), text="Department:", padx=2, pady=2,
                                   bg="Ghost White")
        self.lblDepartment.grid(row=6, column=0, padx=10, sticky=W)
        self.Department_combo = ttk.Combobox(DataFrameLEFT,  textvariable=Department,
                                             values=Departments, font=('arial', 12), width=23)  #state="readonly",
        self.Department_combo.grid(row=6, column=1)
        #self.Department_combo.current(0)

        self.lblL_Center = Label(DataFrameLEFT, font=('arial', 15), text="Local Center:", padx=2, pady=2,
                                 bg="Ghost White")
        self.lblL_Center.grid(row=7, column=0, padx=10, sticky=W)
        self.L_Center_combo = ttk.Combobox(DataFrameLEFT, textvariable=LocalCenter,
                                           values=LocalCenters, font=('arial', 12), width=23)  # state="readonly"
        self.L_Center_combo.grid(row=7, column=1)
        #self.L_Center_combo.current(0)

        self.lblDoB = Label(DataFrameLEFT, font=('arial', 15), text="Date of Birth:", padx=2, pady=2,
                            bg="Ghost White")
        self.lblDoB.grid(row=1, column=2, padx=10, sticky=W)
        today = date.today()
        cal = DateEntry(DataFrameLEFT, font=('arial', 12), width=23, textvariable=DoB, locale='en_US',
                        date_pattern='dd/mm/yyyy',
                        maxdate=today, background='darkblue', foreground='white', borderwidth=2)
        cal.grid(row=1, column=3, padx=10, pady=5)

        self.lblAge = Label(DataFrameLEFT, font=('arial', 15), text="Age:", padx=2, pady=2, bg="Ghost White")
        self.lblAge.grid(row=2, column=2, padx=10, sticky=W)
        self.txtAge = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Age, width=20)
        self.txtAge.grid(row=2, column=3, pady=5)

        self.lblGender = Label(DataFrameLEFT, font=('arial', 15), text="Gender:", padx=2, pady=2,
                               bg="Ghost White")
        self.lblGender.grid(row=3, column=2, padx=10, sticky=W)
        self.Gender_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=Gender,
                                         values=["Select Gender", "Male", "Female"], font=('arial', 12), width=23)
        self.Gender_combo.grid(row=3, column=3)
        self.Gender_combo.current(0)

        self.lblRes_Adr = Label(DataFrameLEFT, font=('arial', 15), text="Res. Address:", padx=2, pady=2,
                                bg="Ghost White")
        self.lblRes_Adr.grid(row=4, column=2, padx=10, sticky=W)
        self.txtRes_Adr = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Res_Address, width=20)
        self.txtRes_Adr.grid(row=4, column=3, pady=5)

        self.lblCity = Label(DataFrameLEFT, font=('arial', 15), text="City:", padx=2, pady=2, bg="Ghost White")
        self.lblCity.grid(row=5, column=2, padx=10, sticky=W)
        self.txtCity = Entry(DataFrameLEFT, font=('arial', 15), textvariable=City, width=20)
        self.txtCity.grid(row=5, column=3, pady=5)

        self.lblRegion = Label(DataFrameLEFT, font=('arial', 15), text="Region:", padx=2, pady=2, bg="Ghost White")
        self.lblRegion.grid(row=6, column=2, padx=10, sticky=W)
        self.Region_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=Region, value=Regions,
                                         font=('arial', 12), width=23)
        self.Region_combo.grid(row=6, column=3)
        self.Region_combo.current(0)

        self.lblCountry = Label(DataFrameLEFT, font=('arial', 15), text="Country:", padx=2, pady=2, bg="Ghost White")
        self.lblCountry.grid(row=7, column=2, padx=10, sticky=W)
        self.txtCountry = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Country, width=20)
        self.txtCountry.grid(row=7, column=3, pady=5)

        self.lblNationality = Label(DataFrameLEFT, font=('arial', 15), text="Nationality:", padx=2, pady=2,
                                    bg="Ghost White")
        self.lblNationality.grid(row=1, column=4, padx=10, sticky=W)
        self.txtNationality = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Nationality, width=20)
        self.txtNationality.grid(row=1, column=5, pady=5)

        self.lblM_Status = Label(DataFrameLEFT, font=('arial', 15), text="Marital Status:", padx=2, pady=2,
                                 bg="Ghost White")
        self.lblM_Status.grid(row=2, column=4, padx=10, sticky=W)
        self.M_Status_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=MaritalStatus,
                                           font=('arial', 12),
                                           width=23, values=["Select Marital Status", "Married", "Single", "Widowed"])
        self.M_Status_combo.grid(row=2, column=5)
        self.M_Status_combo.current(0)

        self.lblEducation = Label(DataFrameLEFT, font=('arial', 15), text="Education", padx=2, pady=2, bg="Ghost White")
        self.lblEducation.grid(row=3, column=4, padx=10, sticky=W)
        self.Education_combo = ttk.Combobox(DataFrameLEFT, state="readonly", textvariable=Education,
                                            values=Education_levels, font=('arial', 12), width=23)
        self.Education_combo.grid(row=3, column=5)
        self.Education_combo.current(0)

        self.lblMobile = Label(DataFrameLEFT, font=('arial', 15), text="Mobile:", padx=2, pady=2, bg="Ghost White")
        self.lblMobile.grid(row=4, column=4, padx=10, sticky=W)
        self.txtMobile = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Mobile, width=20)
        self.txtMobile.grid(row=4, column=5, pady=5)

        self.lblTelephone = Label(DataFrameLEFT, font=('arial', 15), text="Telephone:", padx=2, pady=2,
                                  bg="Ghost White")
        self.lblTelephone.grid(row=5, column=4, padx=10, sticky=W)
        self.txtTelephone = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Telephone, width=20)
        self.txtTelephone.grid(row=5, column=5, pady=5)

        self.lblEmail = Label(DataFrameLEFT, font=('arial', 15), text="Email:", padx=2, pady=2, bg="Ghost White")
        self.lblEmail.grid(row=6, column=4, padx=10, sticky=W)
        self.txtEmail = Entry(DataFrameLEFT, font=('arial', 15), textvariable=Email, width=20)
        self.txtEmail.grid(row=6, column=5, pady=5)

        self.lblOccupation = Label(DataFrameLEFT, font=('arial', 15), text="Occupation:", padx=2, pady=2,
                                   bg="Ghost White")
        self.lblOccupation.grid(row=7, column=4, padx=10, sticky=W)
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

        self.btn_Update = Button(DataFrameLEFT, text="Update", font=('arial', 12, 'bold'), height=1, width=10,
                                 bd=4, bg='#03A9F4', command=Update, cursor='hand2')
        self.btn_Update.grid(row=8, column=4, pady=10)

        self.btnClearDisplay = Button(DataFrameLEFT, text="Clear Display", font=('arial', 12, 'bold'), height=1,
                                      width=10,
                                      bd=4, bg='#03A9F4', command=clearDisplay, cursor='hand2')
        self.btnClearDisplay.grid(row=10, column=3, pady=15)

        # Sync Data Button
        self.sync_icon = ImageTk.PhotoImage(Image.open("sync_icon.jpg"))
        #sync_icon = PhotoImage("sync_icon.jpg")
        self.button_Sync = Button(my_notebook, text="Sync Data Online", image=self.sync_icon, compound=RIGHT, font=('arial', 11), wraplength=130,
                             height=100, width=177, command=Sync_DataOnline)
        self.button_Sync.place(x=2, y=320)

        # exit Button
        exit_image = ImageTk.PhotoImage(Image.open("Exit_icon.jpg"))
        self.btnExit = Button(my_notebook, image=exit_image, height=100, width=177, command=iExit) # changed width from 176
        self.btnExit.image = exit_image
        self.btnExit.place(x=2, y=428)
        # ============================ VIEW TAB ============================================================

        # ===========View Tab Frames===============
        View_MainFrame = Frame(view_tab, bd=1, padx=20, pady=20, relief=RIDGE, bg="Hotpink4", width=get_width*0.87, height=get_height*0.77)
        View_MainFrame.grid(row=0, column=0)   # pack( fill=X, expand=True)

        View_DataFrame = Frame(View_MainFrame, bd=1, padx=10, bg="Ghost white", relief=RIDGE, width=get_width*0.87, height=get_height*0.77)
        View_DataFrame.grid(padx=18, pady=5)  # pack(fill=X, expand=True, padx=10)
        View_DataFrame.grid_columnconfigure(1, weight=1)
        View_DataFrame.grid_propagate(False)
        View_DataFrame.pack_propagate(False)

        View_DataFrameLEFT = Frame(View_DataFrame, bg="Ghost white", relief=RIDGE)
        View_DataFrameLEFT.grid(row=0, column=0)

        View_DataFrameRIGHT = Frame(View_DataFrame, bg="Ghost white", relief=RIDGE)
        View_DataFrameRIGHT.grid(row=0, column=1)

        View_DataFrameLEFT_Top = Frame(View_DataFrameLEFT, bg="Ghost white", relief=RIDGE)
        View_DataFrameLEFT_Top.grid(row=0, column=0, pady=15) #, ipadx=200)

        View_DataFrameLEFT_Bottom = Frame(View_DataFrameLEFT, bg="Ghost white", relief=RIDGE)
        View_DataFrameLEFT_Bottom.grid(row=1, column=0)  #, ipadx=200)

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

        button_clearDisplay2 = Button(View_DataFrameLEFT_Top, text="Clear Display", font=('arial', 12, 'bold'), height=1,
                                    width=10, bd=4, bg='#03A9F4', command=clearDisplay2, cursor='hand2')
        button_clearDisplay2.grid(row=1, column=1, padx=10, pady=10)

        button_Export = Button(View_DataFrameLEFT_Top, text="Export", font=('arial', 12, 'bold'), height=1,
                               width=9, bd=4, bg='turquoise1', command=Export, cursor='hand2')
        button_Export.grid(row=1, column=2, padx=10, pady=10)

        button_Delete = Button(View_DataFrameLEFT_Top, text="Delete", font=('arial', 12, 'bold'), height=1,
                               width=9, bd=4, bg='#03A9F4', command=Delete, cursor='hand2')
        button_Delete.grid(row=1, column=3, padx=10, pady=10)

        # TreeView
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 10, "bold"))
        columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]  # , 24]

        tree = ttk.Treeview(View_DataFrameLEFT_Bottom, selectmode=BROWSE, column=columns, height=30, show='headings',
                            style="mystyle.Treeview")
        tree.grid(row=0, column=0)

        # update profile
        def Edit_profile():
            TreeviewContents = tree.get_children()
            #print(TreeviewContents)
            if TreeviewContents != ():

                response = messagebox.askquestion("CGM Database Management System",
                                                  "Do you want to edit selected profile? \nContinue to member info page to edit.")
                if response == 'yes':
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
                            img = PhotoImage(data=it)  # ImageTk.
                            photo_label.configure(image=img)
                            photo_label.image = img
                            my_notebook.select(0)
                        # print(row)
                    except NameError:
                        pass
                else:
                    return None
            else:
                return None

        def view_worldwide_Data():
            try:
                clearDisplay2()  # clears treeview display
                config = {
                    "apiKey": "AIzaSyAFoAXhsAUVQ0p72EIppjMVDwZJuigldpE",
                    "authDomain": "cgm-database.firebaseapp.com",
                    "databaseURL": "https://cgm-database.firebaseio.com",
                    "projectId": "cgm-database",
                    "storageBucket": "cgm-database.appspot.com",
                    "sagingSenderId": "579778847597",
                    "Id": "1:579778847597:web:a5c20471d3230095403064",
                    "surementId": "G-BK3FR3N448"
                }

                firebase = pyrebase.initialize_app(config)

                # Syncs member Database
                memberDB = firebase.database()
                memberDatabase = "memberDatabase"


                users = memberDB.child(memberDatabase).get()
                vals = users.val()  # gets nested dictionary from firebase
                #print(vals)
                new_vals = {}
                for k in sorted(vals, key=len):
                    new_vals[k] = vals[k]  # gets sorted nested dict by length of keys ie. in ascending order
                #print(new_vals)
                for key in new_vals:
                    #print(key)
                    tree.insert('', END, values=(key, (new_vals[key]["Prefix"]), (new_vals[key]["First name"]), (new_vals[key]["Last name"]),
                                (new_vals[key]["Middle name"]), (new_vals[key]["Position"]), (new_vals[key]["Department"]),
                                (new_vals[key]["Local Center"]), (new_vals[key]["DoB"]), (new_vals[key]["Age"]),
                                (new_vals[key]["Gender"]),(new_vals[key]["Address"]), (new_vals[key]["City"]),
                                (new_vals[key]["Region"]), (new_vals[key]["Country"]), (new_vals[key]["Nationality"]),
                                (new_vals[key]["Marital"]), (new_vals[key]["Education"]), (new_vals[key]["Mobile"]),
                                (new_vals[key]["Telephone"]), (new_vals[key]["Email"]), (new_vals[key]["Occupation"]),
                                (new_vals[key]["Status"])))

            except requests.exceptions.ConnectionError:
                messagebox.showerror("CGM Database Management System",
                                     "Unable to get data.\nPlease check your internet connection and Try again.",
                                     parent=root)
        """
        def element_clicked(event):
            item = tree.focus()
            list2 = (tree.item(item, "values"))
            it = list2[23]
            itz = it.encode()

            #itz = values_list[23]

            img = PhotoImage(data=itz)  # ImageTk.
            photo_labelTop.configure(image=img)
            photo_labelTop.image = img
        """

        # Displays profile from Treeview
        def show(event):
            global selected_ID
            selected_item = tree.selection()[0]  # selection of the first item in Treeview row ie. the ID number
            selected_ID = tree.set(selected_item, '#1')
            #print(selected_ID)
            for row in CGM_DB_BackEnd.searchID(selected_ID):
                global var_ID, it  # useful for query of update_profile function
                var_ID = row[0]
                it = row[23]
                #print(it)
                img = PhotoImage(data=it)  # ImageTk.
                photo_labelTop.configure(image=img)
                photo_labelTop.image = img

            values_list = []
            for line in tree.selection():     #get_children():
                for value in tree.item(line)['values']:
                    values_list.append(value)
                #print(values_list)
                #values_list = tuple(v_list)

                lbl_nameTopValue.configure(text=values_list[2] + ' ' + values_list[4] + ' ' + values_list[3])
                lbl_PositionTopValue.configure(text=values_list[5])
                lbl_DepartmentTopValue.configure(text=values_list[6])
                lbl_LocalCenterTopValue.configure(text=values_list[7])
                lbl_AddressTopValue.configure(text=values_list[11])
                lbl_cityTopValue.configure(text=values_list[12])
                lbl_NationalityTopValue.configure(text=values_list[15])
                lbl_mobileTopValue.configure(text=values_list[18])
                lbl_statusTopValue.configure(text=values_list[22])
                #itz = values_list[23]
                #print(itz)


            """
            for row in CGM_DB_BackEnd.searchID(selected_ID):
                global var_ID, it  # useful for query of update_profile function
                var_ID = row[0]
                lbl_nameTopValue.configure(text=row[2] + ' ' + row[4] + ' ' + row[3])
                lbl_PositionTopValue.configure(text=row[5])
                lbl_DepartmentTopValue.configure(text=row[6])
                lbl_LocalCenterTopValue.configure(text=row[7])
                lbl_AddressTopValue.configure(text=row[11])
                lbl_cityTopValue.configure(text=row[12])
                lbl_NationalityTopValue.configure(text=row[15])
                lbl_mobileTopValue.configure(text=row[18])
                lbl_statusTopValue.configure(text=row[22])
                it = row[23]
                img = PhotoImage(data=it)  # ImageTk.
                photo_labelTop.configure(image=img)
                photo_labelTop.image = img
            """
        tree.bind("<<TreeviewSelect>>", show)  # Displays Profile

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
        tree.heading(21, text="Email", anchor=W)
        tree.heading(22, text="Occupation", anchor=W)
        tree.heading(23, text="Status", anchor=W)
        #tree.heading(24, text="Photo", anchor=W)

        # Tree view columns n sizes
        tree.column(1, width=50, minwidth=80, stretch=True)
        tree.column(2, width=50, minwidth=100, stretch=True)
        tree.column(3, width=50, minwidth=100, stretch=True)  #width=70, minwidth=100
        tree.column(4, width=50, minwidth=100, stretch=True)
        tree.column(5, width=50, minwidth=100, stretch=True)
        tree.column(6, width=50, minwidth=100, stretch=True)
        tree.column(7, width=50, minwidth=100, stretch=True)
        tree.column(8, width=50, minwidth=100, stretch=True)
        tree.column(9, width=50, minwidth=100, stretch=True)
        tree.column(10, width=50, minwidth=100, stretch=True)
        tree.column(11, width=50, minwidth=100, stretch=True)
        tree.column(12, width=50, minwidth=100, stretch=True)
        tree.column(13, width=50, minwidth=100, stretch=True)
        tree.column(14, width=50, minwidth=100, stretch=True)
        tree.column(15, width=50, minwidth=100, stretch=True)
        tree.column(16, width=50, minwidth=100, stretch=True)
        tree.column(17, width=50, minwidth=100, stretch=True)
        tree.column(18, width=50, minwidth=100, stretch=True)
        tree.column(19, width=50, minwidth=100, stretch=True)
        tree.column(20, width=50, minwidth=100, stretch=True)
        tree.column(21, width=50, minwidth=100, stretch=True)
        tree.column(22, width=50, minwidth=100, stretch=True)
        tree.column(23, width=50, minwidth=100, stretch=True)
        #tree.column(24, width=50, minwidth=100, stretch=True)

        # Inserting Scrollbar
        scroll_vertical = ttk.Scrollbar(View_DataFrameLEFT_Bottom, orient="vertical", command=tree.yview)
        scroll_vertical.grid(row=0, column=1, ipady=200)  # (side=RIGHT, fill='y')

        scroll_horizontal = ttk.Scrollbar(View_DataFrameLEFT_Bottom, orient="horizontal", command=tree.xview)
        scroll_horizontal.grid(row=1, column=0, sticky=EW, padx=8, pady=(0, 8))  # (side=BOTTOM, fill='x')

        tree.configure(yscrollcommand=scroll_vertical.set, xscrollcommand=scroll_horizontal.set)

        # view right frame...additional
        right_frame = LabelFrame(View_DataFrameRIGHT, bd=1, padx=5, bg="ghost white", relief=RIDGE, font=('arial', 13, 'bold'),
                                  text="Profile")
        right_frame.grid(row=0, column=0)

        frame_profile = Frame(right_frame, pady=10, bg="ghost white", relief=RIDGE)  # padx=10,
        frame_profile.grid(row=0, column=0, sticky=N)

        # displays Null Image at profile area before ID input
        def displayPhoto():
            global photo_labelTop
            No_photoTop = ImageTk.PhotoImage(Image.open("Null_Image.jpg"))
            photo_labelTop = Label(frame_profile, image=No_photoTop)
            photo_labelTop.image = No_photoTop
            photo_labelTop.grid(row=0, column=0)

        displayPhoto()

        frame_details = Frame(right_frame, pady=5, bg="ghost white", relief=RIDGE)
        frame_details.grid(row=0, column=1)

        lbl_nameTop = Label(frame_details, text="Name :", bg="ghost white")
        lbl_nameTop.grid(row=0, sticky=W, padx=5, pady=5)

        lbl_PositionTop = Label(frame_details, text="Position :", bg="ghost white")
        lbl_PositionTop.grid(row=1, sticky=W, padx=5, pady=5)

        lbl_DepartmentTop = Label(frame_details, text="Department :", bg="ghost white")
        lbl_DepartmentTop.grid(row=2, sticky=W, padx=5, pady=5)

        lbl_LocalCenterTop = Label(frame_details, text="Local Center :", bg="ghost white")
        lbl_LocalCenterTop.grid(row=3, sticky=W, padx=5, pady=5)

        lbl_AddressTop = Label(frame_details, text="Res. Address :", bg="ghost white")
        lbl_AddressTop.grid(row=4, sticky=W, padx=5, pady=5)

        lbl_cityTop = Label(frame_details, text="City :", bg="ghost white")
        lbl_cityTop.grid(row=5, sticky=W, padx=5, pady=5)

        lbl_NationalityTop = Label(frame_details, text="Nationality :", bg="ghost white")
        lbl_NationalityTop.grid(row=6, sticky=W, padx=5, pady=5)

        lbl_mobileTop = Label(frame_details, text="Mobile :", bg="ghost white")
        lbl_mobileTop.grid(row=7, sticky=W, padx=5, pady=5)

        lbl_statusTop = Label(frame_details, text="Status :", bg="ghost white")
        lbl_statusTop.grid(row=8, sticky=W, padx=5, pady=5)


        # profile details values
        lbl_nameTopValue = Label(frame_details, text="", bg="ghost white", width=20, anchor=W)
        lbl_nameTopValue.grid(row=0, column=1, sticky=E, padx=5)

        lbl_PositionTopValue = Label(frame_details, text="", bg="ghost white", width=20, anchor=W)
        lbl_PositionTopValue.grid(row=1, column=1, sticky=E, padx=5)

        lbl_DepartmentTopValue = Label(frame_details, text="", bg="ghost white", width=20, anchor=W)
        lbl_DepartmentTopValue.grid(row=2, column=1, sticky=E, padx=5)

        lbl_LocalCenterTopValue = Label(frame_details, text="", bg="ghost white", width=20, anchor=W)
        lbl_LocalCenterTopValue.grid(row=3, column=1, sticky=E, padx=5)

        lbl_AddressTopValue = Label(frame_details, text="", bg="ghost white", width=20, anchor=W)
        lbl_AddressTopValue.grid(row=4, column=1, sticky=E, padx=5)

        lbl_cityTopValue = Label(frame_details, text="", bg="ghost white", width=20, anchor=W)
        lbl_cityTopValue.grid(row=5, column=1, sticky=E, padx=5)

        lbl_NationalityTopValue = Label(frame_details, text="", bg="ghost white", width=20, anchor=W)
        lbl_NationalityTopValue.grid(row=6, column=1, sticky=E, padx=5)

        lbl_mobileTopValue = Label(frame_details, text="", bg="ghost white", width=20, anchor=W)
        lbl_mobileTopValue.grid(row=7, column=1, sticky=E, padx=5)

        lbl_statusTopValue = Label(frame_details, text="", bg="ghost white", width=20, anchor=W)
        lbl_statusTopValue.grid(row=8, column=1, sticky=E, padx=5)


        profile_button = Button(right_frame, text="Edit Profile", font=('arial', 12, 'bold'), height=1, width=11,
                                bd=4, bg='#03A9F4', cursor='hand2', command=Edit_profile)
        profile_button.grid(row=1, column=1, padx=10, pady=(70, 40))  #, sticky=E)

        viewWorldwide_button = Button(View_DataFrameRIGHT, text="View worldwide Data", font=('arial', 12, 'bold'), height=2, width=12,
                                bd=4, bg='turquoise1', cursor='hand2', wraplength=150, command=view_worldwide_Data)
        viewWorldwide_button.grid(row=1, column=0, padx=10, pady=(40, 40), sticky=S)

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

        def Addnew_Att():
            if (len(ServiceDate.get()) and len(Males.get()) and len(Females.get()) and len(Children.get())
                    and len(TotalAttendance.get()) and len(NewMembers.get()) and len(NewConverts.get()) != 0):
                # #### ADD IF STATEMENTS TO CHECK IF ANY ENTRY IS NOT A NUMBER / DIGIT   ######
                if Males.get().isnumeric() and Females.get().isnumeric() and Children.get().isnumeric() and \
                        TotalAttendance.get().isnumeric() and NewMembers.get().isnumeric() and NewConverts.get().isnumeric():
                    Has_synced = 'false'
                    CGM_DB_Attendance_Backend.addAttendanceRec(ServiceDate.get(), Males.get(), Females.get(),
                                                               Children.get(),
                                                               TotalAttendance.get(), NewMembers.get(),
                                                               NewConverts.get(), Has_synced)
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
                edit_selected_item = tree_Att.selection()[0]  # selection of the first item in Treeview row ie. the ID number
                global Attendance_ListNo
                Attendance_ListNo = tree_Att.set(edit_selected_item, '#1')
                for row in CGM_DB_Attendance_Backend.searchID(Attendance_ListNo):
                    if Attendance_ListNo != '':
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
                    pass
                    #print("first case scenario works")
                    #messagebox.showerror("CGM Database Management System",
                                         #"You can only Update after editing an existing data !!!", parent=root)
                elif (len(ServiceDate.get()) and len(Males.get()) and len(Females.get()) and len(Children.get())
                      and len(TotalAttendance.get()) and len(NewMembers.get()) and len(NewConverts.get()) != 0):
                    if Males.get().isnumeric() and Females.get().isnumeric() and Children.get().isnumeric() and \
                            TotalAttendance.get().isnumeric() and NewMembers.get().isnumeric() and NewConverts.get().isnumeric():
                        Has_synced = 'false'
                        CGM_DB_Attendance_Backend.dataUpdate(Attendance_ListNo, ServiceDate.get(), Males.get(),
                                                             Females.get(), Children.get(), TotalAttendance.get(),
                                                             NewMembers.get(), NewConverts.get(), Has_synced)
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

        def view_worldwide_Attendance():
            try:
                delete_Treeview_AttItems()  # clears treeview display
                config = {
                    "apiKey": "AIzaSyAFoAXhsAUVQ0p72EIppjMVDwZJuigldpE",
                    "authDomain": "cgm-database.firebaseapp.com",
                    "databaseURL": "https://cgm-database.firebaseio.com",
                    "projectId": "cgm-database",
                    "storageBucket": "cgm-database.appspot.com",
                    "sagingSenderId": "579778847597",
                    "Id": "1:579778847597:web:a5c20471d3230095403064",
                    "surementId": "G-BK3FR3N448"
                }

                firebase = pyrebase.initialize_app(config)

                # Syncs attendance Database
                attendanceDB = firebase.database()
                attendanceDatabase = "attendanceDatabase"
                #overall_IDs = []
                paths = attendanceDB.child(attendanceDatabase).get()

                for path in paths.each():
                    #print(path.key())
                    #print(path.val())
                    dict_values = []
                    data = path.val()
                    for value in data.values():
                        dict_values.append(value)  # makes list of values of dictionary
                    #print(dict_values)

                    tree_Att.insert('', END, values=(path.key(), dict_values[0], dict_values[1], dict_values[2], dict_values[3],
                                                 dict_values[4], dict_values[5], dict_values[6]))   #dict_values)

            except requests.exceptions.ConnectionError:
                messagebox.showerror("CGM Database Management System",
                                     "Unable to get data.\nPlease check your internet connection and Try again.",
                                     parent=root)


        def ShowList_Att():
            delete_Treeview_AttItems()
            for row in CGM_DB_Attendance_Backend.viewData():
                tree_Att.insert("", END,
                                values=row)  # (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7])))

        def BarChart_Att():
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

        Attendance_MainFrame = Frame(attendance_tab, padx=20, pady=20, relief=RIDGE, bg="Hotpink4", width=get_width*0.87, height=get_height*0.77)
        Attendance_MainFrame.grid()   # pack()  # side=BOTTOM)  width=1300, height=800,  expand=True, fill=BOTH,

        Attendance_DataFrame = LabelFrame(Attendance_MainFrame, padx=10, pady=10, bg="Ghost white", relief=RIDGE,
                                          font=('arial', 20, 'bold'), text="Attendance\n", width=get_width*0.87, height=get_height*0.77)  # width=1000, height=800,
        Attendance_DataFrame.grid(row=0, column=0, padx=18, pady=5) #, sticky=W)  # , expand=True, fill=BOTH
        Attendance_DataFrame.grid_columnconfigure(1, weight=1)
        Attendance_DataFrame.grid_propagate(False)
        Attendance_DataFrame.pack_propagate(False)

        Attendance_DataFrame_Left = Frame(Attendance_DataFrame, padx=10, pady=10, bg="Ghost white")  # width=1000, height=800,
        Attendance_DataFrame_Left.pack(side=LEFT, anchor=N) # padx=(12, 0))  # fill=BOTH, expand=True,

        Attendance_DataFrame_Left_T = Frame(Attendance_DataFrame_Left, padx=10, pady=10, bg="Ghost white")  # width=1000, height=800,
        Attendance_DataFrame_Left_T.pack(side=TOP, padx=(12, 0))  # fill=BOTH, expand=True,

        Attendance_DataFrame_Left_B = Frame(Attendance_DataFrame_Left, padx=10, pady=10, bg="Ghost white")  # width=1000, height=800,
        Attendance_DataFrame_Left_B.pack(side=BOTTOM, padx=(12, 0))  # fill=BOTH, expand=True,

        Attendance_DataFrame_Right = Frame(Attendance_DataFrame, padx=10, pady=10, bg="Ghost white")  # width=1000, height=800,
        Attendance_DataFrame_Right.pack(side=RIGHT, anchor=N)  # fill=BOTH, expand=True,

        Attendance_DataFrame_Right_T = Frame(Attendance_DataFrame_Right, padx=10, pady=10, bg="Ghost white")  # width=1000, height=800,
        Attendance_DataFrame_Right_T.pack(side=TOP)  # fill=BOTH, expand=True,

        Attendance_DataFrame_Right_B = Frame(Attendance_DataFrame_Right, padx=10, pady=10, bg="Ghost white")  # width=1000, height=800,
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
        lbl_ServiceDate = Label(Attendance_DataFrame_Left_T, font=('arial', 13), text="Date of service:", padx=2, pady=2,
                                bg="Ghost White")
        lbl_ServiceDate.grid(row=0, column=0, padx=(10, 0), pady=20, sticky=W)
        today = date.today()
        S_date = DateEntry(Attendance_DataFrame_Left_T, font=('arial', 15), width=12, textvariable=ServiceDate,
                           locale='en_US',
                           date_pattern='dd/mm/yyyy', maxdate=today, background='darkblue', foreground='white',
                           borderwidth=2)
        S_date.grid(row=0, column=1, padx=10, pady=5)
        # S_date.bind("<FocusIn>", defocus)

        lbl_Males = Label(Attendance_DataFrame_Left_T, font=('arial', 13), text="No. of Males:", padx=2, pady=2,
                          bg="Ghost White")
        lbl_Males.grid(row=1, column=0, padx=(10, 0), pady=20, sticky=W)
        txt_Males = Entry(Attendance_DataFrame_Left_T, font=('arial', 15), textvariable=Males, width=14)
        txt_Males.grid(row=1, column=1, pady=5)

        lbl_Females = Label(Attendance_DataFrame_Left_T, font=('arial', 13), text="No. of Females:", padx=2, pady=2,
                            bg="Ghost White")
        lbl_Females.grid(row=2, column=0, padx=(10, 0), pady=20, sticky=W)
        txt_Females = Entry(Attendance_DataFrame_Left_T, font=('arial', 15), textvariable=Females, width=14)
        txt_Females.grid(row=2, column=1, pady=5)

        lbl_Children = Label(Attendance_DataFrame_Left_T, font=('arial', 13), text="No. of Children:", padx=2, pady=2,
                             bg="Ghost White")
        lbl_Children.grid(row=3, column=0, padx=(10, 0), pady=20, sticky=W)
        txt_Children = Entry(Attendance_DataFrame_Left_T, font=('arial', 15), textvariable=Children, width=14)
        txt_Children.grid(row=3, column=1, pady=5)

        lbl_TotalAttendance = Label(Attendance_DataFrame_Left_T, font=('arial', 13), text="Total Attendance:", padx=2,
                                    pady=2,
                                    bg="Ghost White")
        lbl_TotalAttendance.grid(row=4, column=0, padx=(10, 0), pady=20, sticky=W)
        txt_TotalAttendance = Entry(Attendance_DataFrame_Left_T, font=('arial', 15), textvariable=TotalAttendance,
                                    width=14)
        txt_TotalAttendance.grid(row=4, column=1, pady=5)

        lbl_NewMembers = Label(Attendance_DataFrame_Left_T, font=('arial', 13), text="No. of New Members:", padx=2,
                               pady=2,
                               bg="Ghost White")
        lbl_NewMembers.grid(row=0, column=2, padx=(20, 0), pady=20, sticky=W)
        txt_NewMembers = Entry(Attendance_DataFrame_Left_T, font=('arial', 15), textvariable=NewMembers, width=14)
        txt_NewMembers.grid(row=0, column=3, padx=20, pady=5)

        lbl_NewConverts = Label(Attendance_DataFrame_Left_T, font=('arial', 13), text="No. of New Converts:", padx=2,
                                pady=2,
                                bg="Ghost White")
        lbl_NewConverts.grid(row=1, column=2, padx=(20, 0), pady=20, sticky=W)
        txt_NewConverts = Entry(Attendance_DataFrame_Left_T, font=('arial', 15), textvariable=NewConverts, width=14)
        txt_NewConverts.grid(row=1, column=3, padx=20, pady=5)

        # =============== Attendance page Buttons ======================
        # left frame buttons
        btnClearEntry_Att = Button(Attendance_DataFrame_Left_T, text="Clear Entry", font=('arial', 12, 'bold'), height=1,
                                   width=9,
                                   bd=4, bg='#03A9F4', command=ClearEntry_Att, cursor='hand2')
        btnClearEntry_Att.grid(row=6, column=0, pady=50)

        btnSubmit_Att = Button(Attendance_DataFrame_Left_T, text="Submit", font=('arial', 12, 'bold'), height=1, width=9,
                               bd=4, bg='#03A9F4', command=Addnew_Att, cursor='hand2')
        btnSubmit_Att.grid(row=6, column=1, pady=50)

        btnUpdate_Att = Button(Attendance_DataFrame_Left_T, text="Update", font=('arial', 12, 'bold'), height=1, width=9,
                               bd=4, bg='#03A9F4', command=Update_Att, cursor='hand2')
        btnUpdate_Att.grid(row=6, column=3, pady=50)

        btnEdit_Att = Button(Attendance_DataFrame_Left_T, text="Edit", font=('arial', 12, 'bold'), height=1, width=9,
                             bd=4, bg='#03A9F4', command=Edit_Att, cursor='hand2')
        btnEdit_Att.grid(row=6, column=2, pady=50)



        viewWorldwide_buttonAtt = Button(Attendance_DataFrame_Left_B, text="View worldwide Attendance", font=('arial', 12, 'bold'),
                                      height=2, width=12, pady=5,
                                      bd=4, bg='turquoise1', cursor='hand2', wraplength=150, command=view_worldwide_Attendance)
        viewWorldwide_buttonAtt.grid(row=0, column=1, padx=10, pady=(40, 40))  #, sticky=S)

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