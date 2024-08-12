import mysql.connector

class MYSQLDB:
    
    def __init__(self):
        self.mydb = mysql.connector.connect(
        host="10.76.76.77",
        user="kostya_hrorder",
        password="yJSVm)W[si*yDXO8",
        database="kostya_hrorder")

        self.curs = self.mydb.cursor()
    #


    def searchorders(self, startordertime, endordertime):
        
        querystr = 'SELECT `empid`, `ordercapt`,`ordertext` FROM `ordertab` WHERE `ordertime` BETWEEN %(startordertime)s AND %(endordertime)s AND `state`= 1' 

        queryvals= dict()
       
        queryvals["startordertime"] = startordertime
        queryvals["endordertime"] = endordertime

        self.curs.execute(querystr,queryvals)
        
        return self.curs.fetchall()
    #
