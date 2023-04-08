from webscraper import WebScraper as ws

class NationalParks:
    def __init__(self, url="", group="", soup=True):
        self.locations = []
        self.group = group
        self.url = url
        self.wsGroup = ws(url = self.url, group=self.group)
        self.soup = soup

    def GetListParks(self):
        if self.group == "NSWNP":
            for element in self.wsGroup.get_soup().find_all("li",{"class":"headingIcon icon tree visit"}):
                self.locations.append({
                    "name": element.get_text().strip(),
                    "url": element.a["href"].strip(),
                    "campings": []
                })
        return self.locations

    def GetParkInfo(self, index=0, url=""):
        wsPark = ws(url=url)
        for element in wsPark.get_soup().find_all("div",{"class":"scrollingBox__item camping"}):
            self.locations[index]["campings"].append(self.url + element.a["href"].strip())

    def ParksInfo(self):
        if self.soup:
            for idx, park in enumerate(self.GetListParks()):
                self.GetParkInfo(idx, park["url"])
            
            return self.locations
        
    def GetCampingInfo(self, url=""):
        wsCamping = ws(url=url)
        wsCampingMap = ws(url=url+"/visitor-info")

        items = wsCamping.get_soup().find("table",{"class":"itemDetails"}).find_all("tr")
        details = {}

        for item in items:
            rows = item.findChildren(['th', 'td'])
            details[rows[0].get_text()] = rows[1].get_text().strip()

        new_camping = {
            "name": wsCamping.get_soup().find("h1",{"class":"show-inline"}).get_text().strip(),
            "location": wsCamping.get_soup().find("p",{"class":"tabbedPageSubTitle"}).get_text().strip(),
            "map_url": self.url + wsCampingMap.get_soup().find("li",{"class":"headingIcon icon pdf"}).a["href"],
            "details": details
        }
        print(new_camping)

########################################
if __name__ == "__main__":
    print("Debug: National Parks module")


