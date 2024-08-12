import custom
import numpy
import pandas as pd

#תשלום נסיעות ללא סמל שכר יסוד

def pubtrasport_nowork(level="0"):

    arrpubtrans = custom.DF101.loc[(custom.DF101["Elem"].isin(custom.pubtransport))&(custom.DF101["CurAmount"]>0)&(custom.DF101["Refdate"] == custom.REFMONTH),"Empid_mn"].unique()
    arryesod = custom.DF101.loc[(custom.DF101['Elem'].isin(custom.yesodandhours))&(custom.DF101["CurAmount"]>0)&(custom.DF101["Refdate"] == custom.REFMONTH),"Empid_mn"].unique()
    diffarr = numpy.setdiff1d(arrpubtrans,arryesod,assume_unique=True)
    
    resdf = custom.DF101[(custom.DF101["Empid_mn"].isin(diffarr))&(custom.DF101["Elem"].isin(custom.yesodandhours+custom.pubtransport))][["Empid","Empname","mn","Elem_heb","CurAmount","CurQuantity"]]
    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם עובד","mn":"מנ","Elem_heb":"סמל","CurAmount":"סכום","CurQuantity":"כמות"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="pubtrasport_no_work",index=False)
    #

    return len(resdf)
#