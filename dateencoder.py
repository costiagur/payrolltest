import json
import datetime

# stringify date to json

class dateEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime):
                    return obj.strftime("%Y-%m-%d")
                # Let the base class default method raise the TypeError
                return json.JSONEncoder.default(self, obj)
            #
        #

#jsonfile = "{}{}{}".format(".\\jsondfs\\",refmonth.strftime("%Y-%m"),".json")

        
                                        
#with open(jsonfile,mode="w") as fp:
#        json.dump(df.to_dict(orient='list'),fp,cls=dateEncoder)
#