# הפחתות שעות גדולות גם רטרו.
import custom
import pandas as pd

def semel_hourdeduct(level="100"):

    level = float(level)
    
    middf = custom.DF101.loc[(custom.DF101["Elem"].isin((custom.hourdeduct,custom.semelnett))&(custom.DF101["Elemtype"].isin(["additional data","addition components"])))][["Empid","Empname","Elem","Refdate","CurAmount","CurQuantity"]]
    middf["Nett"] = middf.apply(lambda row:row["CurAmount"] if row["Elem"] == custom.semelnett else 0, axis=1 )
    middf["Hourdeduct"] = middf.apply(lambda row:row["CurQuantity"] if row["Elem"] == custom.hourdeduct else 0, axis=1 )
    groupdf = middf.groupby(by=["Empid","Empname"],as_index=False,group_keys=True).sum(["Nett","Hourdeduct"])
    filtereddf = groupdf.loc[((groupdf["Nett"]<1000)&(groupdf["Hourdeduct"]>10))|(groupdf["Hourdeduct"]>level),"Empid"]
    
    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.loc[(middf["Empid"].isin(filtereddf))&((middf["Hourdeduct"] != 0)|(middf["Nett"] != 0)),["Empid","Empname","Refdate","Nett","Hourdeduct"]].to_excel(writer,sheet_name="large_hourdeduct",index=False)
    #    

    return len(filtereddf.unique())
#