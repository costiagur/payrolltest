#בדיקה שך סכום הביטוח אינו עולה על הסכום המרבי
import custom
import pandas as pd


def licinsveh(level="1779,1750,7000"):

    middf = custom.DF101.loc[custom.DF101["Elem"].isin(custom.lics+custom.instotal),["Empid","Empname","Elem","Elem_heb","PrevAmount","CurAmount"]]
    middf["Lic"] = middf.apply(lambda row: row["PrevAmount"]+row["CurAmount"] if row["Elem"] in custom.lics else 0, axis=1)
    middf["Inshova"] = middf.apply(lambda row: row["PrevAmount"]+row["CurAmount"] if row["Elem"] in custom.inshova else 0, axis=1)
    middf["Instotal"] = middf.apply(lambda row: row["PrevAmount"]+row["CurAmount"] if row["Elem"] in custom.instotal else 0, axis=1)
    middf["Both"] = middf.apply(lambda row: 1 if abs(row["PrevAmount"]) > 0 and abs(row["CurAmount"])>0 else 0, axis=1)

    levellist = level.split(",")

    licamount = float(levellist[0])
    hovaamount = float(levellist[1])
    insamount = float(levellist[2])

    groupdf = middf.groupby(by = ["Empid","Empname"],as_index=False,group_keys=True).sum(("Lic","Inshova","Instotal","Both"))
    filteredempid = groupdf.loc[(groupdf["Lic"]>licamount)|(groupdf["Inshova"]>hovaamount)|(groupdf["Instotal"]>insamount)|(groupdf["Both"]>0),"Empid"].unique()

    middf.rename(columns={"Empname":"שם","Empid":"מספר עובד","Elem":"סמל","Elem_heb":"שם סמל","PrevAmount":"סכום חודש קודם","CurAmount":"סכום שוטף","Lic":"רישיון","Inshova":"חובה","Instotal":"חובה ומקיף"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.loc[middf["מספר עובד"].isin(filteredempid),["מספר עובד","שם","שם סמל","סכום חודש קודם","סכום שוטף","רישיון","חובה","חובה ומקיף"]].to_excel(writer,sheet_name="רישיון וביטוח רכב",index=False)
    #  

    return len(filteredempid)
#
    