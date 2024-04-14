#סמלים שמופיעים פעם אחת
import custom
import pandas as pd

def semelonce(level="0.05"):

    level = float(level)

    middf = custom.DF101.loc[(custom.DF101["Division"]!= 90)&(custom.DF101["Refdate"]==custom.REFMONTH)&(custom.DF101["CurAmount"]!=0)&(custom.DF101["Elemtype"]=="addition components")&(~custom.DF101["Elem"].isin((custom.annualvehicle+custom.miluim))),["Rank","Dirug","Elem","Elem_heb","CurAmount","Empid"]]

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

    resdf = middf.loc[middf["filter"] == True]

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="semel_once",index=False)
    # 
        

    return resdf.shape[0]

#