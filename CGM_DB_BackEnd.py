import sqlite3


def memberData():
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS memberCGM (id INTEGER PRIMARY KEY, Prefix text, Firstname text, Surname text, \
                MiddleName text, ChurchPosition text, Department text, LocalCenter text, DoB text, Age text, Gender text, \
                 Address text, City text, Region text, Country text, Nationality text, MaritalStatus text, Education text, \
                 Mobile text, Telephone text, Email text, Occupation text, ChurchStatus text, Photo Blob)")
    con.commit()
    con.close()


def addMemberRec(Prefix, Firstname, Surname, MiddleName, ChurchPosition, Department, LocalCenter, DoB, Age, Gender,
                 Address, City, Region, Country, Nationality, MaritalStatus, Education, Mobile, Telephone, Email,
                 Occupation, ChurchStatus, Photo):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("INSERT INTO memberCGM VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (Prefix, Firstname, Surname, MiddleName, ChurchPosition, Department, LocalCenter, DoB, Age, Gender,
                 Address, City, Region, Country, Nationality, MaritalStatus, Education, Mobile, Telephone, Email,
                 Occupation, ChurchStatus, Photo))
    con.commit()
    con.close()


def viewData():
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM")
    rows = cur.fetchall()
    con.close()
    return rows

"""
def searchFirstname(Firstname=""):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Firstname=?", (Firstname,))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows
"""

def searchFirstname(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Firstname LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchSurname(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Surname LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchMiddlename(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE MiddleName LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchPosition(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE ChurchPosition LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchDepartment(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Department LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchLocalCenter(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE LocalCenter LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchAge(Age=""):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Age=?", (Age,))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchGender(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Gender LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchCity(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE City LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchRegion(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Region LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchCountry(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Country LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchNationality(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Nationality LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchEducation(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Education LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchOccupation(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE Occupation LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def searchChurchStatus(input):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE ChurchStatus LIKE '{}%'".format(input))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def deleteRec(id):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("DELETE FROM memberCGM WHERE id=?", (id,))
    con.commit()
    con.close()


# ==========TOP LEVEL (Profile pop up)=============
def searchID(ID=""):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM memberCGM WHERE ID=?", (ID,))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def dataUpdate(id, Prefix="", Firstname="", Surname="", MiddleName="", ChurchPosition="", Department="", LocalCenter="",
               DoB="", Age="",  Gender="", Address="", City="", Region="", Country="", Nationality="", MaritalStatus="",
               Education="", Mobile="", Telephone="", Email="", Occupation="", ChurchStatus="", Photo=""):
    con = sqlite3.connect("memberCGM.db")
    cur = con.cursor()
    cur.execute("UPDATE memberCGM SET Prefix=?, Firstname=?, Surname=?, MiddleName=?, ChurchPosition=?, Department=?, LocalCenter=?,"
                " DoB=?, Age=?,  Gender=?, Address=?, City=?, Region=?, Country=?, Nationality=?, MaritalStatus=?, Education=?,"
                " Mobile=?, Telephone=?, Email=?, Occupation=?, ChurchStatus=?, Photo=? WHERE id=?", (Prefix, Firstname,
                 Surname, MiddleName, ChurchPosition, Department, LocalCenter, DoB, Age, Gender, Address, City, Region,
                 Country, Nationality, MaritalStatus, Education, Mobile, Telephone, Email, Occupation, ChurchStatus, Photo, id))
    con.commit()
    con.close()


memberData()