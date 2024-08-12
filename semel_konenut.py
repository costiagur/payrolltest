#כוננות בחוזה אישי
import custom
import pandas as pd

def semel_konenut(level="0"):  
    middf = custom.DF101[(custom.DF101["Refdate"] == custom.REFMONTH)&(custom.DF101["Rank"].isin(custom.hozeishi))&((custom.DF101["Elem"] == custom.konenut)&(custom.DF101["CurQuantity"] > 0))]

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf = middf[["Empid","Empname","Dirug","Elem_heb","CurQuantity"]].copy()
        resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Dirug":"דירוג","Elem_heb":"סמל","CurQuantity":"כמות"},inplace=True)
        middf[["Empid","Empname","Dirug","Elem_heb","CurQuantity"]].to_excel(writer,sheet_name="כוננות בחוזה אישי",index=False)
    # 
        
    return len(middf)