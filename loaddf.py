import pandas as pd
from io import BytesIO
import sqlite3
import re
import custom

def loaddf(filesdict,reqfiletype="new"): 

    currhazutidf = None
    prevhazutidf = None

    tomessage = []

    if len(filesdict) > 0:
       
        dbcon = sqlite3.connect(custom.dbsave)
        cur = dbcon.cursor()

        def hazutfiles(buff,filename):
            cols = list(range(5,23,1))
            cols = cols + [2,3]
                
            midDF = pd.read_csv(buff,sep='\t',header=3,encoding="cp1255",na_filter=True,skip_blank_lines=True,skiprows=[5],usecols=cols,dtype={14:str},parse_dates=['תאריך ערך','ת.ת. עבודה',"הפסקה מ","הפסקה עד"],dayfirst=True)

            midDF.rename(columns={"שם עובד":"Empname","מספר עובד":"Empid","מ.נ.":"mn","אגף":"Division","סכום":"Amount","כמות":"Quantity","תאריך ערך":"Refdate","ת.ת. עבודה":"Startdate","סוג רכיב":"Elemtype_heb","שם רכיב":"Elem_heb","דרוג":"Dirug","דרגה":"darga","וותק":"vetek","הפסקה מ":"Stopfrom","הפסקה עד":"Stoptill","סמל הפסקה":"Stopcode","שם הפסקה":"Stopname"},inplace=True)

            midDF.dropna(axis=0,subset=['Amount','Quantity'],inplace=True) #drop rows with no amount or quantity

            midDF["Elem"] = midDF["Elem_heb"].str.extract(r'^(\d+|עלות)\s-*') #extract element num or incase of alut which is without number, seti it to alut. Therefore it is str.
            midDF["Rank"] = midDF["Dirug"].str.extract(r'(\d+)') #extract rank number
            midDF["Empid_mn"] = midDF[["Empid","mn"]].apply(lambda a: "{}_{}".format(a["Empid"],a["mn"]), axis=1)
            midDF["Ind"] = midDF.apply(lambda x: "{}_{}_{}".format(x["Empid_mn"], x["Elem"], x["Refdate"].strftime('%Y%m%d')), axis=1)
            midDF["Refdate"] = midDF['Refdate'].dt.date
            midDF["Startdate"] = midDF['Startdate'].dt.date
            midDF["Stopfrom"] = midDF['Stopfrom'].dt.date
            midDF["Stoptill"] = midDF['Stoptill'].dt.date

            fromconv = ["מספר ותאור רכיבי תוספות","מספר ותאור רכיבי ניכויי חובה","מספר ותאור רכיבי ניכויי רשות","מספר ותאור רכיבי הפרשות","נתונים נוספים","מספר ותאור  רכיבי זקיפות הטבה"]
            toconv = ["addition components","compulsory deductions","voluntary deductions","provision components","additional data","benefit charge components"]

            midDF["Elemtype"] = midDF["Elemtype_heb"]
            midDF["Elemtype"] = midDF["Elemtype"].replace(to_replace = fromconv, value=toconv)

            midDF.sort_values(by=["Empid","mn","Elemtype","Elem","Refdate"],ascending=[True,True,True,True,False],axis=0,ignore_index=True,inplace=True)
            
            global tomessage
            tomessage = f"רשומות חדשות {'בחזותי חודש שוטף' if filename=='currhazuti' else 'בחזותי חודש קודם'}: {str(midDF.shape[0])}"

            return (midDF, tomessage)
        #
        
        def timesheetfile(buff,filename):
            df = pd.read_csv(buff,sep='\t',header=2,encoding="cp1255",na_filter=False,skip_blank_lines=True,parse_dates=['תאריך נוכחות'],dayfirst=True)

            for eachtitle in df.columns:
                midval = re.sub(r'[^a-zA-Zא-ת\d\s]',"",eachtitle)
                midval = midval.strip()
                midval = re.sub(r'\s+','_',midval)
                df.rename(columns={eachtitle:midval},inplace=True)
            #

            df.drop(columns=['משרד','מונה_קיזוז1'],inplace=True)

            if len(df.columns[df.columns.str.contains('Unnamed')]) > 0:
                df.drop(columns=df.columns[df.columns.str.contains('Unnamed')],inplace=True)
            #

            df.rename(columns={"מחלקה":"אגף","מחלקה1":"מחלקה"},inplace=True)

            empty_name_cols = [col for col in df.columns if col == '' or col is None]

            if len(empty_name_cols) > 0:
                df.drop(columns=empty_name_cols,inplace=True)
            #

            #print(df.columns)

            df["תאריך_נוכחות"] = df["תאריך_נוכחות"].dt.date

            def strtutimenum(strdata):
                if strdata == "":
                    return 0
                elif type(strdata) == str:
                    if re.search(r'\d',strdata) and re.search(r':',strdata):
                        return float(strdata.split(':')[0])+round(float(strdata.split(':')[1])/60,2)
                    else:
                        return strdata
                else:
                    return strdata 
            #
            
            df.iloc[:,8:df.shape[1]] = df.iloc[:,8:df.shape[1]].map(strtutimenum,na_action='ignore')

            df.loc[df["פעילות"] == ".................","פעילות"] = "עבודה"

            msg = df.to_sql("timesheet",dbcon,if_exists='replace',chunksize=500,method='multi')

            return f"מספר רשומות נוכחות הינו {str(msg)}"
        #

        def jobs(buff, filename):
            midDF = pd.read_csv(buff,sep='\t',header=0,encoding="cp1255",na_filter=True,skip_blank_lines=True,parse_dates=['תוקף מ','תוקף עד'],dayfirst=True)
            midDF.rename(columns={"שם עובד":"empname","מספר זהות ":"empid","מ.נ":"mn","תוקף מ":"datefrom","תוקף עד":"datetill","תפקיד":"jobnum","שם תפקיד":"jobname","תיאור תפקיד":"jobdescript"},inplace=True)
            midDF["empid_mn"] = midDF[["empid","mn"]].apply(lambda a: "{}_{}".format(a["empid"],a["mn"]), axis=1)
            msg = midDF.to_sql("jobs",dbcon,if_exists='replace',chunksize=500,method='multi')
            query = """
                WITH doublejobs AS ( 
                SELECT *, COUNT(empid_mn), min(datefrom) as mindatefrom, empid_mn||'_'||REPLACE(datefrom,"00:00:00","") AS deleterow FROM jobs
                GROUP BY empid_mn
                HAVING COUNT(empid_mn) > 1 AND datefrom = min(datefrom)
                )
                DELETE FROM jobs
                WHERE empid_mn||'_'||REPLACE(datefrom,"00:00:00","") IN (SELECT deleterow FROM doublejobs)
                """
            cur.execute(query) #מחיקת מקרים בהם לאותו עובד יש שני תפקידים. מוחקים את המוקדם מביניהם
            dbcon.commit()
            return f"מספר רשומות תפקידים הינו {str(msg)}"
        #

        for eachfile in dict(sorted(filesdict.items(),reverse=True)):             
            if eachfile == "currhazuti" and reqfiletype == "new":
                buff = BytesIO(filesdict['currhazuti'][1])
                currhazutidf, msg = hazutfiles(buff,eachfile)
                tomessage.append(msg)
                if isinstance(currhazutidf,pd.DataFrame):
                    currhazutidf.set_index('Ind', inplace=True)
                    currhazutidf.to_sql("dfcurr",dbcon,if_exists='replace',index=True, chunksize=500)
            #

            elif eachfile == "currhazuti" and reqfiletype == "addreplace":
                buff = BytesIO(filesdict['currhazuti'][1])
                smalldf, msg = hazutfiles(buff,eachfile)
                tomessage.append(msg)
                if isinstance(smalldf,pd.DataFrame):
                    delexist = "DELETE FROM dfcurr WHERE Empid_mn IN " + str(tuple(smalldf["Empid_in"].unique()))
                    cur.execute(delexist)
                    dbcon.commit()
                    smalldf.to_sql("dfcurr",dbcon,if_exists='append',index=True,chunksize=500)
                    print("data added/replaced in currhazuti")
            #

            elif eachfile == "prevhazuti":
                buff = BytesIO(filesdict['prevhazuti'][1])
                prevhazutidf, msg = hazutfiles(buff,eachfile)
                tomessage.append(msg)
                if isinstance(prevhazutidf,pd.DataFrame):
                    prevhazutidf.set_index('Ind', inplace=True)
                    prevhazutidf.to_sql("dfprev",dbcon,if_exists='replace',index=True,chunksize=500)
            #

            elif eachfile == "timeschedulefile":
                buff = BytesIO(filesdict['timeschedulefile'][1])
                msg = timesheetfile(buff,eachfile)
                tomessage.append(msg)
            #
            
            elif eachfile == "jobs":
                buff = BytesIO(filesdict['jobs'][1])
                msg = jobs(buff,eachfile)
                tomessage.append(msg)
            #
        #


        if "currhazuti" not in filesdict: #test if there is currhazuti data to work with
            if cur.execute("""SELECT tbl_name FROM sqlite_schema WHERE type='table' AND tbl_name='dfcurr'; """).fetchall():
                pass
            else:
                tomessage.append("לא קיימות רשומות חודש שוטף במערכת ")
            #
        #
        if "prevhazuti" not in filesdict: #test if there is prevhazuti data to work with
            if cur.execute("""SELECT tbl_name FROM sqlite_schema WHERE type='table' AND tbl_name='dfprev'; """).fetchall():
                pass
            else:
                tomessage.append("לא קיימות רשומות חודש קודם במערכת ")
            #
        #

        if "timeschedulefile" not in filesdict: #test if there is hours data to work with
            if cur.execute("""SELECT tbl_name FROM sqlite_schema WHERE type='table' AND tbl_name='timesheet'; """).fetchall():
                pass
            else:
                tomessage.append("לא קיימות רשומות שעות עבודה במערכת ")

            #
        #

        if "jobs" not in filesdict: #test if there is hours data to work with
            if cur.execute("""SELECT tbl_name FROM sqlite_schema WHERE type='table' AND tbl_name='jobs'; """).fetchall():
                pass
            else:
                tomessage.append("לא קיימות רשומות תפקידים במערכת ")

            #
        #

        timesheetmonth = cur.execute("""SELECT DATE((SELECT MAX(timesheet.תאריך_נוכחות) from timesheet),'start of month')""").fetchone()[0]                               
        currdfmonth = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

        if currdfmonth != timesheetmonth:
            tomessage.append(f"אזהרה: קיימות רשומות שעות עבודה מתאריך {timesheetmonth} בעוד שהרשומות בתלוש שייכות לתאריך {currdfmonth} ")
        #

        dbcon.close()

    return '; '.join(tomessage)

#