#הזינו סכום במקום כמות בסמל שעות עבודה בשכר לפי שעות
import custom
import pandas as pd

def semel_payhours(level="177"):

    level = float(level)

    middf = custom.DF101[(custom.DF101["Refdate"] == custom.REFMONTH)&((custom.DF101["Elem"] == custom.byhourpay)&(custom.DF101["CurQuantity"] > level))][["Empid","Empname","mn","Elem_heb","CurQuantity"]]
    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.to_excel(writer,sheet_name="payhours_toohigh",index=False)
    # 

    return len(middf)
#