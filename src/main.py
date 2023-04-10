from nationalparks import NationalParks as NP
from database import Database as db
import asyncio

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

urls = urls_pipeline.next()["allurls"]

for url in urls:
    Camping = NP.GetCampingInfo(url)

    if Camping:
        NP.available_campings.append(Camping)
        print("Info: Progression {}/{} ({})".format(len(NP.available_campings),len(urls),Camping["name"]))

if NP.available_campings: 
    myDb.insert_many("nationalparks_campings", NP.available_campings, True)
    print("Info: Rejected campings {}".format(NP.unavailable_campings))