from webscraper import WebScraper as ws
from database import Database as db

class NationalParks:
    def __init__(self, url="", group=""):
        self.locations = []
        self.group = group
        self.url = url
        self.wsGroup = ws(url = self.url, group=self.group)

    def GetListParks(self):
        if self.group == "NSWNP":
            for element in self.wsGroup.get_soup().find_all("li",{"class":"headingIcon icon tree visit"}):
                self.locations.append({
                    "name": element.get_text().strip(),
                    "url": element.a["href"].strip(),
                    "campings": []
                })
        return self.locations

    def ParksInfo(self):
        for idx, park in enumerate(self.GetListParks()):
            self.GetParkInfo(idx, park["url"])
        
        return self.locations

    def GetParkInfo(self, index=0, url=""):
        wsPark = ws(url=url)
        for element in wsPark.get_soup().find_all("div",{"class":"scrollingBox__item camping"}):
            self.locations[index]["campings"].append(self.url + element.a["href"].strip())

########################################
if __name__ == "__main__":
    myDb = db()
    CollectNationalParks = True

    # National Parks
    if CollectNationalParks:
        NP = NationalParks(url="https://www.nationalparks.nsw.gov.au", group="NSWNP")
        listParks = NP.ParksInfo()
        myDb.insert_many("nationalparks", listParks, True)
    else: print("Info: Skip National Parks")


