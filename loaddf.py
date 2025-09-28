import pandas as pd
import custom
from io import BytesIO
import os
import sqlite3

def loaddf(filesdict,reqfiletype="new"): 

    tomessage = []

    if len(filesdict) > 0:

        #unsortedDFHOURS = pd.DataFrame(columns=["Empid","Empname","mn","Refdate","WorkHours","Empid_mn","Elem"])
        
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

            #print(midDF.columns) 

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
            #

        #
            #
        if reqfiletype == "new":
            
            # Hours - concat, remove duplicates, insert in DB or picle
            
            unsortedDFHOURS = pd.concat([hoursquery1313df,hoursquery1307df],ignore_index=True)
            sorteddf = unsortedDFHOURS.sort_values(by='WorkHours', ascending=False)              
            DFHOURS = sorteddf.drop_duplicates(subset='Empid_mn', keep='first',ignore_index=True)
            DFHOURS.set_index('Ind', inplace=True)
            #custom.DFHOURS = DFHOURS
            #pd.to_pickle(custom.DFHOURS,r'drafts\dfhours.pkl')
            DFHOURS.to_sql("dfhours",dbcon,if_exists='replace',index=True,method='multi')

            # Currhazuti - merge with hours, insert in DB or pickle
            
            DFCURR = pd.merge(currhazutidf,DFHOURS['WorkHours'],how="left",on="Ind")
            DFCURR.set_index('Ind', inplace=True)
            #custom.DFCURR = DFCURR
            #custom.REFMONTH = DFCURR["Refdate"].max()
            #pd.to_pickle(custom.DFCURR, r'drafts\dfcurr.pkl')
            
            print(DFCURR.columns)
            
            DFCURR.to_sql("dfcurr",dbcon,if_exists='replace',index=True, chunksize=500)
            
            # Prevhazuti - insert in DB or pickle
            
            prevhazutidf.set_index('Ind', inplace=True)
            #custom.DFPREV = prevhazutidf
            #custom.PREVMONTH = custom.DFPREV["Refdate"].max()
            #pd.to_pickle(custom.DFPREV, r'drafts\dfprev.pkl')
            prevhazutidf.to_sql("dfprev",dbcon,if_exists='replace',index=True,chunksize=500)
    
            print("data loaded as new")

        elif reqfiletype == "addreplace":
            if eachfile == "currhazuti":
                smalldf = pd.merge(currhazutidf,DFHOURS,how="left",on="Ind")

                delexist = "DELETE FROM dfcurr WHERE Empid_mn IN " + str(tuple(smalldf["Empid_in"].unique()))
                
                DFCURR = pd.read_sql("SELECT * FROM dfcurr",dbcon)

                cur.execute(delexist)
                dbcon.commit()

                smalldf.to_sql("dfcurr",dbcon,if_exists='append',index=True)

                #DFCURR.drop(existdf.loc[existdf["Empid"].isin(midDF101["Empid"].unique())].index,inplace=True)
                #existdf = pd.concat([existdf,smalldf],ignore_index=True)
                #existdf.sort_values(by=["Empid","mn","Elemtype","Elem","Refdate"],ascending=[True,True,True,True,False],axis=0,ignore_index=True,inplace=True)
                #pd.to_pickle(existdf,r'drafts\dfcurr.pkl' if eachfile == "currhazuti" else r'drafts\dfprev.pkl')

                print("data added/replaced in currhazuti")
                #
            #
        #

        if "currhazuti" not in filesdict:
            #if "dfcurr.pkl" in9 os.listdir("drafts"):
            #    custom.DFCURR = pd.read_pickle('drafts/dfcurr.pkl')
            #    custom.REFMONTH = custom.DFCURR["Refdate"].max()
            if cur.execute("""SELECT tableName FROM sqlite_master WHERE type='table' AND tableName='dfcurr'; """).fetchall():
                pass
            else:
                tomessage.append("לא קיימות רשומות חודש שוטף במערכת ")
            #
        #
        if "prevhazuti" not in filesdict:
            #if "dfprev.pkl" in os.listdir("drafts"):
            #    custom.DFPREV = pd.read_pickle('drafts/dfprev.pkl')
            #    custom.PREVMONTH = custom.DFPREV["Refdate"].max()
            if cur.execute("""SELECT tableName FROM sqlite_master WHERE type='table' AND tableName='dfprev'; """).fetchall():
                pass
            else:
                tomessage.append("לא קיימות רשומות חודש קודם במערכת ")
            #
        #
        if "hoursquery1313" not in filesdict and "hoursquery1307" not in filesdict:
            #if "dfhours.pkl" in os.listdir("drafts"):
            #    custom.DFHOURS = pd.read_pickle('drafts/dfhours.pkl')
            #
            if cur.execute("""SELECT tableName FROM sqlite_master WHERE type='table' AND tableName='dfhours'; """).fetchall():
                pass
            else:
                tomessage.append("לא קיימות רשומות שעות עבודה במערכת ")
            #
        #
    
        dbcon.close()
    #
    #else:
    #    custom.DFCURR = pd.read_pickle('drafts/dfcurr.pkl')
    #    custom.DFPREV = pd.read_pickle('drafts/dfprev.pkl')
    #    custom.DFHOURS = pd.read_pickle('drafts/dfhours.pkl')
    #    custom.REFMONTH = custom.DFCURR["Refdate"].max()
    #    custom.PREVMONTH = custom.DFPREV["Refdate"].max()
    #

   
    #print(r'\n'.join(tomessage))
    return '; '.join(tomessage)

#