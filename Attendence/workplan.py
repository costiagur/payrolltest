import custom
import pandas as pd
import sqlite3
import inspect
from scipy import stats

def workplan(level = "0"):
    conn = sqlite3.connect(custom.dbsave)

    query = """
    SELECT timesheet.מספר_עובד, timesheet.יום, GROUP_CONCAT(timesheet.שעות_100,',') as extra100, GROUP_CONCAT(timesheet.שנ_100_לא_מאוש,',') as extra100nonpay
    from timesheet 
    where timesheet.מספר_עובד in 
    (SELECT timesheet.מספר_עובד from timesheet 
        WHERE timesheet.פעילות = 'עבודה' 
        GROUP BY timesheet.מספר_עובד 
        HAVING (SUM(timesheet.שעות_100) + SUM(timesheet.שנ_100_לא_מאוש))> 4)
    AND timesheet.פעילות = 'עבודה' AND timesheet.מש_20 = 0
    group by  timesheet.מספר_עובד, timesheet.יום
    """

    middf = pd.read_sql_query(query, conn)

    middf.set_index(['מספר_עובד','יום'],inplace=True)

    newdf = middf.unstack(level=-1,)

    newdf.fillna('0,0,0,0,0',inplace=True)

    def kruskaltest(row):
        daylist = []

        for eachday in ['א','ב','ג','ד','ה','ו']:
            rowlistA = row['extra100'][eachday].split(',')
            rowlistB = row['extra100nonpay'][eachday].split(',')

            rowlistA = [float(A) for A in rowlistA]
            rowlistB = [float(B) for B in rowlistB]

            rowlist = [a + b for a,b in zip(rowlistA,rowlistB)]

            if len([eachval for eachval in rowlist if eachval > 0]) > 2: # only arrays of 3 or more existing vals > 0
                daylist.append(rowlist)
            else:
                pass
        #

        checkset = set([max(eachlist) for eachlist in daylist])
        #if all values are identical
        if len(checkset) <= 1:
            return (0,0.5)
        else:
            statis = stats.kruskal(*daylist) 
            return statis
        #
    #

    newdf[['kruskalval','kruskalprob']] = newdf[['extra100','extra100nonpay']].apply(kruskaltest,result_type='expand',axis=1)

    oveddf = newdf.loc[(newdf['kruskalprob']>=0.9)|(newdf['kruskalprob']<=0.1),['kruskalval','kruskalprob']].copy()
    oveddf.reset_index(inplace=True)


    query = f"""SELECT timesheet.מספר_עובד, timesheet.שם_עובד,timesheet.מחלקה,timesheet.תאריך_נוכחות, timesheet.יום,timesheet.פעילות, timesheet.שעות_100, timesheet.שנ_100_לא_מאוש 
    FROM timesheet 
    WHERE timesheet.מספר_עובד in {str(tuple(oveddf['מספר_עובד']))} AND timesheet.פעילות = 'עבודה' 
    GROUP BY timesheet.מספר_עובד,timesheet.תאריך_נוכחות  
    HAVING timesheet.שעות_100 + timesheet. שנ_100_לא_מאוש > 0.4 AND timesheet.מש_20 = 0
    """

    resdf = pd.read_sql_query(query, conn)

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='overlay') as writer:
        resdf.to_excel(writer,sheet_name="סטיות תכנית עבודה",index=False,startrow=1,header=True)
    # 

    conn.close

    return [inspect.stack()[0][3],resdf.shape[0],"סטיות תכנית עבודה"]
#
