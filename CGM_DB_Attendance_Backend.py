import sqlite3

def attendanceData():
    con = sqlite3.connect("attendanceCGM.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS attendanceCGM (id INTEGER PRIMARY KEY, ServiceDate text, Males text, \
                Females text, Children text, TotalAttendance text, NewMembers text, NewConverts text, Has_synced text)")
    con.commit()
    con.close()


def addAttendanceRec(ServiceDate, Males, Females, Children, TotalAttendance, NewMembers, NewConverts, Has_synced):
    con = sqlite3.connect("attendanceCGM.db")
    cur = con.cursor()
    cur.execute("INSERT INTO attendanceCGM VALUES (NULL, ?,?,?,?,?,?,?,?)",
                (ServiceDate, Males, Females, Children, TotalAttendance, NewMembers, NewConverts, Has_synced))
    con.commit()
    con.close()


def viewData():
    con = sqlite3.connect("attendanceCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM attendanceCGM")
    rows = cur.fetchall()
    con.close()
    return rows


def deleteRec(id):
    con = sqlite3.connect("attendanceCGM.db")
    cur = con.cursor()
    cur.execute("DELETE FROM attendanceCGM WHERE id=?", (id,))
    con.commit()
    con.close()


def dataUpdate(id, ServiceDate="", Males="", Females="", Children="", TotalAttendance="", NewMembers="", NewConverts="", Has_synced=""):
    con = sqlite3.connect("attendanceCGM.db")
    cur = con.cursor()
    cur.execute("UPDATE attendanceCGM SET ServiceDate=?, Males=?, Females=?, Children=?, TotalAttendance=?,"
                "NewMembers=?,  NewConverts=?, Has_synced=? WHERE id=?",
                (ServiceDate, Males, Females, Children, TotalAttendance, NewMembers, NewConverts, Has_synced, id))
    con.commit()
    con.close()


def searchID(ID=""):
    con = sqlite3.connect("attendanceCGM.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM attendanceCGM WHERE ID=?", (ID,))
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def getServiceDate():
    con = sqlite3.connect("attendanceCGM.db")
    cur = con.cursor()
    cur.execute("SELECT ServiceDate FROM attendanceCGM")
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


def getTotalAttendance():
    con = sqlite3.connect("attendanceCGM.db")
    cur = con.cursor()
    cur.execute("SELECT TotalAttendance FROM attendanceCGM")
    rows = cur.fetchall()
    if not rows:
        rows = ("not found",)
    con.close()
    return rows


attendanceData()