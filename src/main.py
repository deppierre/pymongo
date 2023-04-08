from nationalparks import NationalParks as NP
from database import Database as db

# Database
myDb = db()

# National Parks
NP = NP(url="https://www.nationalparks.nsw.gov.au", group="NSWNP", soup=False)
listParks = NP.ParksInfo()

if listParks: myDb.insert_many("nationalparks", listParks, True)
else: print("Info: Skip National Parks collection")

# Campings
urls_pipeline = myDb.agg("nationalparks",
[
    {
        "$group" : {
            "_id" : None,
            "campings": { "$push": "$campings" }
        }
    },
    {
        "$project": {
            "_id": 0,
            "allurls": {
                "$reduce": {
                    "input": "$campings",
                    "initialValue": [],
                    "in": {
                        "$concatArrays": [
                            "$$value",
                            "$$this" 
                        ]
                    }
                }
            }
        }
    }
])

for url in urls_pipeline.next()["allurls"]: 
    NP.GetCampingInfo(url)
