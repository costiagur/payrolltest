#סמלים שמופיעים פעם אחת
import custom
import pandas as pd

def semelonce(level="0.05"):

    level = float(level)

    middf = custom.DF101.loc[(custom.DF101["Division"]!= 90)&(custom.DF101["Refdate"]==custom.REFMONTH)&(custom.DF101["CurAmount"]!=0)&(custom.DF101["Elemtype"]=="addition components")&(~custom.DF101["Elem"].isin((custom.annualvehicle+custom.miluim))),["Rank","Dirug","Elem","Elem_heb","CurAmount","Empid","Empname"]]

    groupdf = middf.groupby(by=["Rank","Dirug","Elem"],as_index=False,group_keys=True).count()
    groupempdf = middf.groupby(by="Rank",as_index=False,group_keys=True).nunique()

    groupempdf["bench"] = groupempdf["Empid"] * level

    def getbench(row):
        return groupempdf.loc[groupempdf["Rank"] == row["Rank"],"bench"].item()

    groupdf["bench"] = groupdf.apply(getbench, axis=1)

    filterdf = groupdf.loc[(groupdf["CurAmount"]<4)&(groupdf["CurAmount"]<groupdf["bench"])]

    def filterrow(row):
        return filterdf.loc[(filterdf["Elem"] == row["Elem"])&(filterdf["Rank"] == row["Rank"])].shape[0] > 0


    middf["filter"] = middf.apply(filterrow,axis=1)

    middf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Elem":"מספר סמל","Elem_heb":"סמל שכר","filter":"מסנן","Dirug":"דירוג","Rank":"דרגה","CurAmount":"סכום שוטף"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.loc[middf["מסנן"] == True, ["מספר עובד","שם","סמל שכר","סכום שוטף"]].to_excel(writer,sheet_name="סמל ייחודי",index=False)
    # 
        

    return  middf.loc[middf["מסנן"] == True].shape[0]

#