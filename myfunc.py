import base64
import json
import common
from io import BytesIO
from datetime import date
from openpyxl import Workbook
import custom

from loaddf import loaddf

from Payment.totalrep import totalrep
from Payment.pubtrasport_nowork import pubtrasport_nowork
from Payment.pubtransport_leasing import pubtransport_leasing
from Payment.no_pubtransport import no_pubtransport
from Payment.semel_ratio import semel_ratio
from Payment.BasisvsCalculated import BasisvsCalculated
from Payment.semel_payhours import semel_payhours
from Payment.semel_cantbe import semel_cantbe
from Payment.semel_hourdeduct import semel_hourdeduct
from Payment.semel6666 import semel6666
from Payment.globalpay import globalpay
from Payment.hightax import hightax
from Payment.semelonce import semelonce
from Payment.fundscount import fundscount
from Payment.vehicle_annual import vehicle_annual
from Payment.hoursWithoutYesod import hoursWithoutYesod
from Payment.highgrossbtl import highgrossbtl
from Payment.before9months import before9months
from Payment.NonreasonableNett import NonreasonableNett
from Payment.semel_without import semel_without
from Payment.nettnegative import nettnegative
from Payment.rationonbase import rationonbase
from Payment.ratelow import ratelow
from Payment.analysis13m import analysis13m
from Payment.onecompare import onecompare
from Payment.currpmt_to_left_emps import currpmt_to_left_emps
from Payment.deductyesod import deductyesod
from Payment.longabscent import longabscent
from Payment.newsymbols import newsymbols
from Payment.NettAboveGross import NettAboveGross

from Llm.llmquery import llmquery
from Db.sqlquery import sqlquery

from Attendence.diff_time2pay import diff_time2pay
from Attendence.many_extrahours import many_extrahours
from Attendence.morethan12 import morethan12
from Attendence.workplan import workplan
from Attendence.nonauthhours import nonauthhours
from Attendence.shabat import shabat
from Attendence.manyhours import manyhours
from Attendence.paidabscence import paidabscence
from Attendence.vehnopresence import vehnopresence

def myfunc(queryobj):
#    try:
        postdict = queryobj._POST()
        filesdict = queryobj._FILES()      

        request = postdict["request"]

        if custom.xlresfile is None:
            custom.xlresfile = BytesIO()
            wb = Workbook()
            wb.save(custom.xlresfile)
        else:
            pass # continue using the same file
        #

        if request == "fileupload":
            res = loaddf(filesdict,postdict["reqfiletype"])
            replymsg = json.dumps(["uploadedrows",res]).encode('UTF-8')


        elif request == "salarycheck":

            replymsg = b""

            reqtest = postdict["reqtest"]
            reqlevel = postdict["reqlevel"]
                        
            checkpool = {}

            checkpool["semel_cantbe"] = semel_cantbe
            checkpool["semel_payhours"] = semel_payhours
            checkpool["semel_hourdeduct"] = semel_hourdeduct
            checkpool["pubtrasport_nowork"] = pubtrasport_nowork
            checkpool["pubtransport_leasing"] = pubtransport_leasing
            checkpool["no_pubtransport"] = no_pubtransport
            checkpool["semel6666"] = semel6666
            checkpool["globalpay"] = globalpay
            checkpool["semel_ratio"] = semel_ratio
            checkpool["BasisvsCalculated"] = BasisvsCalculated
            checkpool["vehicle_annual"] = vehicle_annual
            checkpool["semelonce"] = semelonce
            checkpool["hightax"] = hightax
            checkpool["fundscount"] = fundscount
            checkpool["hoursWithoutYesod"] = hoursWithoutYesod
            checkpool["manyhours"] = manyhours
            checkpool["highgrossbtl"] = highgrossbtl
            checkpool["before9months"] = before9months
            checkpool["totalrep"] = totalrep
            checkpool["NonreasonableNett"] = NonreasonableNett
            checkpool["semel_without"] = semel_without
            checkpool["nettnegative"] = nettnegative
            checkpool["rationonbase"] = rationonbase
            checkpool["ratelow"] = ratelow
            checkpool["newsymbols"] = newsymbols
            checkpool["diff_time2pay"] = diff_time2pay
            checkpool["many_extrahours"] = many_extrahours
            checkpool["morethan12"] = morethan12
            checkpool["workplan"] = workplan
            checkpool["currpmt_to_left_emps"] = currpmt_to_left_emps
            checkpool["nonauthhours"] = nonauthhours
            checkpool["shabat"] = shabat
            checkpool["deductyesod"] = deductyesod
            checkpool["longabscent"] = longabscent
            checkpool["paidabscence"] = paidabscence
            checkpool["NettAboveGross"] = NettAboveGross
            checkpool["vehnopresence"] = vehnopresence

            res = checkpool[reqtest](reqlevel)
            replymsg = json.dumps([res[0],res[1],res[2]]).encode('UTF-8')


        elif request == "testfile": #request for the resulting XL file with all the tests
                        
            f = custom.xlresfile
            f.seek(0)
            file64enc = base64.b64encode(f.read())
            file64dec = file64enc.decode()
            replymsg = json.dumps(["testfile",r'report_' + date.today().strftime('%Y%m%d') + ".xlsx",file64dec]).encode('UTF-8') #f.name
            custom.xlresfile = None
        #

        elif request == "hazuti13m":   
            file64enc = base64.b64encode(analysis13m(filesdict,postdict["expectedplus"]))
            file64dec = file64enc.decode()
            replymsg = json.dumps(["outliers.xlsx",file64dec]).encode('UTF-8')
        #

        elif request == "onecompare":
            resdf = onecompare(postdict["empid"])
            replymsg = json.dumps(["oneperson",resdf]).encode('UTF-8')
        #

        elif request == "llmquery":
            restxt = llmquery(postdict["myrequest"],postdict["reqtype"])
            replymsg = json.dumps([postdict["reqtype"],restxt]).encode('UTF-8')
        #
        
        elif request == "sqlquery":
            if postdict["how"] == 'show':
                resjson = sqlquery(postdict["myrequest"],postdict["source"],'show')
                replymsg = json.dumps(resjson).encode('UTF-8')
            elif postdict["how"] == 'xls':
                file64enc = base64.b64encode(sqlquery(postdict["myrequest"],postdict["source"],'xls'))
                file64dec = file64enc.decode()
                replymsg = json.dumps(["Result",['resoutput.xlsx',file64dec]]).encode('UTF-8')
            #
        #

        return replymsg
 
            # reply message should be encoded to be sent back to browser ----------------------------------------------
            # encoding to base64 is used to send ansi hebrew data. it is decoded to become string and put into json.
            # json is encoded to be sent to browser.
            #    file64enc = base64.b64encode(filesdict['doc1'][1])
            #    file64dec = file64enc.decode()
  

    #
    
#    except Exception as e:
#        common.errormsg(title=__name__,message=e)
#        replymsg = json.dumps(["Error","myfunc -" + str(e)]).encode('UTF-8')
#        return replymsg
    #
#