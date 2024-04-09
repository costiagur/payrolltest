#סמלים שמופיעים פעם אחת
import numpy as np
import custom
import pandas as pd

def semelonce(level="0.05"):

    level = float(level)

    middf = custom.DF101.loc[(custom.DF101["Division"] != custom.pensiondepartment)&(custom.DF101["Refdate"]==custom.REFMONTH)&(custom.DF101["CurAmount"] != 0)&(custom.DF101["Elemtype"] == "addition components")]

    empinranks = middf[["Rank","Empid"]].groupby(by = ["Rank"],as_index=False,group_keys=True).nunique("Empid")

    empinranks["cutoff"] = empinranks.apply(lambda row: np.round(row["Empid"]*level,0),axis=1)

    uniqsemels = middf[middf["Rank"].isin(empinranks.loc[empinranks["cutoff"] > 0,"Rank"])].groupby(by = ["Rank","Elem"],as_index=False,group_keys=True).count()

    uniqsemels["uniq"] = uniqsemels.apply(lambda row:empinranks.loc[empinranks["Rank"]==row["Rank"],"cutoff"].item(),axis=1)
    uniqsemels["todrop"] = uniqsemels.apply(lambda row:True if row["Empid"] > row["uniq"] else False,axis=1)

    uniqsemels.drop(uniqsemels[uniqsemels["todrop"] == True].index,inplace=True)

    uniqsemels.drop(["todrop","uniq"],axis=1,inplace=True)

    def isuniq(row):
        res = uniqsemels.loc[(uniqsemels["Rank"] == row["Rank"])&(uniqsemels["Elem"] == row["Elem"]),"Elem"]
        if res.size != 0:
            return True
        else:
            return False
        #
    #
 
    resdf = middf.loc[middf.apply(isuniq,axis=1) == True]

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="semel_once",index=False)
    # 
        

    return resdf.shape[0]

#