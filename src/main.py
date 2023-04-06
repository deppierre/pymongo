from nationalparks import NationalParks as NP
from database import Database as db

# Database
myDb = db()

# National Parks
NP = NP(url="https://www.nationalparks.nsw.gov.au", group="NSWNP", soup=False)
listParks = NP.ParksInfo()

if listParks: myDb.insert_many("nationalparks", listParks, True)
else: print("Info: Skip National Parks")

campings = myDb.query_find("nationalparks", query="{ campings:{$ne:[]} }", projection="{ campings:1 }")
print(campings)