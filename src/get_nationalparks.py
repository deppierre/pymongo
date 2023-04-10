import nationalparks as NP
import database as db
from dotenv import dotenv_values

# National Parks
config = dotenv_values("../.env")
url = config["ROOT_URL"]

listParks = NP.ParksInfo(url)

if listParks: db.insert_many("nationalparks", listParks, True)
else: print("Info: Skip National Parks collection")