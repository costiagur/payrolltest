#בדיקה שך סכום הביטוח אינו עולה על הסכום המרבי
import custom
import pandas as pd


def licinsveh(level="1779,1750,7000"):

    middf = custom.DF101.loc[custom.DF101["Elem"].isin(custom.lics+custom.instotal),["Empname","Empid","Elem","Elem_heb","PrevAmount","CurAmount"]]
    middf["Lic"] = middf.apply(lambda row: row["PrevAmount"]+row["CurAmount"] if row["Elem"] in custom.lics else 0, axis=1)
    middf["Inshova"] = middf.apply(lambda row: row["PrevAmount"]+row["CurAmount"] if row["Elem"] in custom.inshova else 0, axis=1)
    middf["Instotal"] = middf.apply(lambda row: row["PrevAmount"]+row["CurAmount"] if row["Elem"] in custom.instotal else 0, axis=1)

    levellist = level.split(",")

    licamount = float(levellist[0])
    hovaamount = float(levellist[1])
    insamount = float(levellist[2])

    groupdf = middf.groupby(by = ["Empid","Empname"],as_index=False,group_keys=True).sum(("Lic","Inshova","Instotal"))
    filteredempid = groupdf.loc[(groupdf["Lic"]>licamount)|(groupdf["Inshova"]>hovaamount)|(groupdf["Instotal"]>insamount),"Empid"].unique()

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.loc[middf["Empid"].isin(filteredempid)].to_excel(writer,sheet_name="RishayonBituahRehev",index=False)
    #  


    return len(filteredempid)
#
    