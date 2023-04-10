import nationalparks as NP
import database as db

def GetCampings():

    available_campings = []
    unavailable_campings = []

    # Campings
    # NP = NP(url="https://www.nationalparks.nsw.gov.au", group="NSWNP", soup=False)
    urls_pipeline = db.agg("nationalparks",
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
    if len(urls) > 0:
        for url in urls:
            Camping = NP.GetCampingInfo(url,True)

            if Camping:
                available_campings.append(Camping)
                print("Info: Progression {}/{} ({})".format(len(available_campings),len(urls),Camping["name"]))
            else:
                unavailable_campings.append(url)

        if available_campings: 
            db.insert_many("nationalparks_campings", available_campings, True)
            print("Info: Rejected campings {}".format(unavailable_campings))
        
        return 1
    else:
        print("Info: No National Park found")
        return 0

if __name__ == "__main__":
    GetCampings()