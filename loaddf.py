import pandas as pd
import custom
from io import BytesIO

def loaddf(filesdict):
    if custom.DF101 is not None:
        pass
    else: 
        buff = BytesIO(filesdict['hazuti'][1])

        cols = list(range(5,21,1))
        cols = cols + [2,3]
            
        custom.DF101 = pd.read_csv(buff,sep='\t',header=3,encoding="cp1255",na_filter=True,skip_blank_lines=True,skiprows=[5],usecols=cols,parse_dates=['תאריך ערך','ת.ת. עבודה'],dayfirst=True)
                
        custom.DF101.rename(columns={"שם עובד":"Empname","מספר עובד":"Empid","מ.נ.":"mn","אגף":"Division","סכום":"PrevAmount","כמות":"PrevQuantity",custom.DF101.columns[16]:"CurAmount",custom.DF101.columns[17]:"CurQuantity","תאריך ערך":"Refdate","ת.ת. עבודה":"Startdate","סוג רכיב":"Elemtype_heb","שם רכיב":"Elem_heb","דרוג":"Dirug"},inplace=True)

        custom.DF101["Elem"] = custom.DF101["Elem_heb"].str.extract(r'^(\d+|עלות)\s-*')
        custom.DF101["Rank"] = custom.DF101["Dirug"].str.extract('(\d+)')
        custom.DF101["Empid_mn"] = custom.DF101[["Empid","mn"]].apply(lambda a: "{}_{}".format(a["Empid"],a["mn"]), axis=1)

        fromconv = ["מספר ותאור רכיבי תוספות","מספר ותאור רכיבי ניכויי חובה","מספר ותאור רכיבי ניכויי רשות","מספר ותאור רכיבי הפרשות","נתונים נוספים","מספר ותאור  רכיבי זקיפות הטבה"]
        toconv = ["addition components","compulsory deductions","voluntary deductions","provision components","additional data","benefit charge components"]

        custom.DF101["Elemtype"] = custom.DF101["Elemtype_heb"]
        custom.DF101["Elemtype"].replace(to_replace = fromconv, value=toconv,inplace=True)

        custom.DF101.dropna(axis=0,subset=['PrevAmount','PrevQuantity','CurAmount','CurQuantity'],inplace=True)
                
        custom.REFMONTH = custom.DF101["Refdate"].max()
        custom.PREVMONTH = pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = -1)
    #
    if custom.DFHOURS is not None:
        pass
    else:
        buff = BytesIO(filesdict['hoursquery'][1])

        custom.DFHOURS = pd.read_csv(buff,sep='\t',header=0,encoding="cp1255",na_filter=True,skip_blank_lines=True,parse_dates=['תוקף עד','תוקף מ'],dayfirst=True,usecols=list(range(0,6,1)))
        custom.DFHOURS.rename(columns={"מספר זהות ":"Empid","שם עובד":"Empname","מ.נ":"mn","תוקף מ":"Refdate","תוקף עד":"Enddate","כמות":"WorkHours"}, inplace=True)
        custom.DFHOURS["Empid_mn"] = custom.DFHOURS[["Empid","mn"]].apply(lambda a: "{}_{}".format(a["Empid"],a["mn"]), axis=1)                            
        custom.DFHOURS["Elem"] = custom.yesod
        custom.DFHOURS.drop(columns="Enddate",inplace=True)
        #custom.DF101["CurQuantity"] =custom.DF101.apply(lambda row: custom.DFHOURS.loc[(custom.DFHOURS["Empid_mn"] == row["Empid_mn"]),"Quantity"].sum() if row["Refdate"] == custom.REFMONTH and row["Elem"] == custom.yesod else row["CurQuantity"],axis=1)

        custom.DF101 = pd.merge(custom.DF101,custom.DFHOURS,how="left",on=["Empid_mn","Elem","Empid","mn","Empname","Refdate"])


    #

    print(custom.DF101.shape[0])
    return custom.DF101.shape[0]

#