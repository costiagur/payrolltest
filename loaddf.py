import pandas as pd
import custom
from io import BytesIO
import os
import sqlite3
import re

def loaddf(filesdict,reqfiletype="new"): 

    hoursquery1313df = None
    hoursquery1307df = None
    currhazutidf = None
    prevhazutidf = None

    tomessage = []

    if len(filesdict) > 0:
       
        dbcon = sqlite3.connect('dbsave.db')
        cur = dbcon.cursor()
        DFHOURS = None
        unsortedDFHOURS = None

        def houfiles(buff,filename):
            midDFHOURS = pd.read_csv(buff,sep='\t',header=0,encoding="cp1255",na_filter=True,skip_blank_lines=True,parse_dates=['תוקף עד','תוקף מ'],dayfirst=True,usecols=list(range(0,6,1)))
            midDFHOURS.rename(columns={"מספר זהות ":"Empid","שם עובד":"Empname","מ.נ":"mn","תוקף מ":"Refdate","תוקף עד":"Enddate","כמות":"WorkHours"}, inplace=True)
            midDFHOURS["Empid_mn"] = midDFHOURS[["Empid","mn"]].apply(lambda a: "{}_{}".format(a["Empid"],a["mn"]), axis=1)                            
            midDFHOURS["Elem"] = custom.yesod
            midDFHOURS.drop(columns="Enddate",inplace=True)
            midDFHOURS["Ind"] = midDFHOURS.apply(lambda x: "{}_{}_{}".format(x["Empid_mn"], x["Elem"], x["Refdate"].strftime('%Y%m%d')), axis=1)
            midDFHOURS["Refdate"] = midDFHOURS['Refdate'].dt.date
            tomessage = f"רשומות {filename}: {str(midDFHOURS.shape[0])}"

            return (midDFHOURS, tomessage)
        #

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
            tomessage = f"רשומות חדשות {filename}: {str(midDF.shape[0])}"

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

            empty_name_cols = [col for col in df.columns if col == '' or col is None]

            if len(empty_name_cols) > 0:
                df.drop(columns=empty_name_cols,inplace=True)
            #

            print(df.columns)


            #df['weekday'] = df['יום'].map({"א":"1","ב":"2","ג":"3","ד":"4","ה":"5","ו":"6","ש":"7"})
            #df["empdate"] = df["מספר_עובד"].astype(str)+"-"+df["תאריך_נוכחות"].astype(str)
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

            df.iloc[:,8:48] = df.iloc[:,8:48].map(strtutimenum,na_action='ignore')

            df.loc[df["פעילות"] == ".................","פעילות"] = "עבודה"

            msg = df.to_sql("timesheet",dbcon,if_exists='replace',chunksize=500,method='multi')

            return f"מספר רשומות נוכחות הינו {str(msg)}"


        for eachfile in dict(sorted(filesdict.items(),reverse=True)):             
            if eachfile == "hoursquery1313":
                buff = BytesIO(filesdict['hoursquery1313'][1])
                hoursquery1313df, msg = houfiles(buff,eachfile)
                tomessage.append(msg)
            elif eachfile == "hoursquery1307":
                buff = BytesIO(filesdict['hoursquery1307'][1])
                hoursquery1307df, msg = houfiles(buff,eachfile)
                tomessage.append(msg)
            elif eachfile == "currhazuti":
                buff = BytesIO(filesdict['currhazuti'][1])
                currhazutidf, msg = hazutfiles(buff,eachfile)
                tomessage.append(msg)
            elif eachfile == "prevhazuti":
                buff = BytesIO(filesdict['prevhazuti'][1])
                prevhazutidf, msg = hazutfiles(buff,eachfile)
                tomessage.append(msg)
            elif eachfile == "timesheetfile":
                buff = BytesIO(filesdict['timesheetfile'][1])
                msg = timesheetfile(buff,eachfile)
                tomessage.append(msg)
            #

        #
            #
        if reqfiletype == "new":
            
            # Hours - concat, remove duplicates, insert in DB or picle
            if hoursquery1313df and hoursquery1307df:
                unsortedDFHOURS = pd.concat([hoursquery1313df,hoursquery1307df],ignore_index=True)
                sorteddf = unsortedDFHOURS.sort_values(by='WorkHours', ascending=False)              
                DFHOURS = sorteddf.drop_duplicates(subset='Empid_mn', keep='first',ignore_index=True)
                DFHOURS.set_index('Ind', inplace=True)
                DFHOURS.to_sql("dfhours",dbcon,if_exists='replace',index=True,method='multi')

            # Currhazuti - merge with hours, insert in DB or pickle

            if currhazutidf:
                if DFHOURS is None:
                    DFHOURS = pd.read_sql("SELECT * FROM dfhours",dbcon)
                    DFHOURS.set_index('Ind', inplace=True)
                #
                DFCURR = pd.merge(currhazutidf,DFHOURS['WorkHours'],how="left",on="Ind")
                DFCURR.set_index('Ind', inplace=True)
                DFCURR.to_sql("dfcurr",dbcon,if_exists='replace',index=True, chunksize=500)
            
            # Prevhazuti - insert in DB or pickle
            
            if prevhazutidf:
                prevhazutidf.set_index('Ind', inplace=True)
                prevhazutidf.to_sql("dfprev",dbcon,if_exists='replace',index=True,chunksize=500)
    
            else:
                pass #in case only timesheet was loaded

        elif reqfiletype == "addreplace":
            if eachfile == "currhazuti":
                smalldf = pd.merge(currhazutidf,DFHOURS,how="left",on="Ind")

                delexist = "DELETE FROM dfcurr WHERE Empid_mn IN " + str(tuple(smalldf["Empid_in"].unique()))
                
                DFCURR = pd.read_sql("SELECT * FROM dfcurr",dbcon)

                cur.execute(delexist)
                dbcon.commit()

                smalldf.to_sql("dfcurr",dbcon,if_exists='append',index=True)

                print("data added/replaced in currhazuti")
                #
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
        if "hoursquery1313" not in filesdict and "hoursquery1307" not in filesdict: #test if there is hours data to work with
            if cur.execute("""SELECT tbl_name FROM sqlite_schema WHERE type='table' AND tbl_name='dfhours'; """).fetchall():
                pass
            else:
                tomessage.append("לא קיימות רשומות שעות עבודה במערכת ")
            #
        #
    
        dbcon.close()

    return '; '.join(tomessage)

#