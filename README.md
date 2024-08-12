# מערכת לבקרת נתוני שכר, השוואה בין שני חודשי שכר ומציאת שינויים בלתי סבירים
המערכת מקבלת דוח חזותי או דוח 101, מחברת אליו נתוני שעות עבודה ומפיקה דוח נתוני שכר עובדים נטו וברוטו, השוואה מול חודש קודם והצגה מאלו סעיפי שכר מורכבים ההפרשים הגדולים. אם נעשה שימוש גם במערכת הוראות שכר (https://github.com/costiagur/HRdirective)[HRdirective], אז הדוח יציג ליד כל רשומת עובד את הוראות השכר שניתנו לגביו במהלך החודש. כך, תהליך הבקרה מפחית צורך להתרוצץ בין מקורות מדיע שונים כדי להין את מקור ההפרשים. כל הנתונים מתרכזים בתצוגה אחת. אפשר גם לבדוק אם השינוי בשכר כצפוי ביחס להוראה שניתנה. 

בנוסף, המערכת מפיקה קובץ אקסל הכולל את דוח נטו עם פירוט הפרשי ברוטו ורטרו גדולים ובדיקות נוספות כלהלן.
המערכת מודולרית, כך שאפשר להוסיף בדיקות חדשות או לגרוע בדיקות קיימות.
בין הבדיקות הקיימות:
1. תשלום שעות כוננות לעובדים בחוזה אישי
2. תשלום נסיעות לעובדים ללא שעות עבודה
3. שיעור משרה העולה על 100%
4. תשלום שעות רגילות בכמות העולה על 177 (או רף אחר כפי שיקבע)
5. ניכוי שעות בכמות חריגה (גבוה מעבר לסביר)
6. יחס לא סביר בין ערך שעה לבסיס הפנסיה, מה שעלול לרמוז על אי התאמה ביניהם, מקדם חלוקה לא מתאים, רכיבים שאינם כפופים לחלקיות משרה וכד'
7. סמלי שכר נדירים לדירוג
8. מציאת עובדים ללא סמלים שיש ליתר העובדים בדירוג
9. תשלום שעות עבודה בכמות חריגה (גבוהה מאוד, בהתחשב בשעות כוננות)
10. שעות נוכחות ללא תשלום שכר
11. ברוטו ביטוח לאומי מעל לתקרה החייבת בביטוח לאומי
12. ניכויי קופות (דווח סכומים שליליים) רטוראקטיביים לתקופה העולה על 9 חודשים אחורה
13. שיעור מס וביטוח לאומי חריגים בסכומם, ביחס רוחבי, או בהתנהגות על פני שתי תקופות
14. שיעורי ניכוי (מעבר למס הכנסה וביטוח לאומי) בשיעור מצטבר גבוה מדי
15. פירוט הפרשי רטרו גבוהים
16. פירוט פערי ברוטו שוטפים גבוהים
17. מציאת מקרים של יחס לא סביר בין שכר נטו לשכר משולב, ברמת דירוג.
# בקרת הפרשה לקופות עבר שאינן קיימות לעובד בשוטף
המערכת יכולה לקבל דוח קופות ולזהות מקרים של הפרשות לקופות רטרואקטיביות לעובד, אשר הפרשותיו השוטפות הולכות לקופות אחרות. המערכת מציעה תיקוני עיתוי בסכומי ברוטו כדי למנוע הפרשות לקופות שאינן קיימות.

## הערה:
סמלי שכר עלולים להיות יחודיים ללקוח ומבני דוחות יכולים להשתנות בין מערכות שכר. לפיכך, נדרשת התאמה של הבקרות וקליטת הדוחות, לפני תחילת השימוש במערכת.


