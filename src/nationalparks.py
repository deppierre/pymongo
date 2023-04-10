from webscraper import WebScraper as ws

class NationalParks:
    def __init__(self, url="", group="", soup=True):
        self.locations = []
        self.group = group
        self.url = url
        self.wsGroup = ws(url = self.url, group=self.group)
        self.soup = soup
        self.available_campings = []
        self.unavailable_campings = []

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
        
    def GetCampingInfo(self, url="",debug=False):
        if debug: print("Debug: GetCampingInfo(url={})".format(url))

        wsCamping = ws(url=url)
        # wsCampingMap = ws(url=url+"/visitor-info")
        new_camping = {}

        # if wsCampingMap:
        #     new_camping["map_url"] = self.url + wsCampingMap.get_soup().find("li",{"class":"headingIcon icon pdf"}).a["href"]
        # else:
        #     new_camping["map_url"] = self.url + wsCamping.get_soup().find("li",{"class":"headingIcon icon pdf"}).a["href"]

        try:
            new_camping["name"] = wsCamping.get_soup().find("h1",{"class":"show-inline"}).get_text().strip()
            new_camping["location"] = wsCamping.get_soup().find("p",{"class":"tabbedPageSubTitle"}).get_text().strip()
            new_camping["url"] = url
            new_camping["status"] = "opened"

            if not wsCamping.get_soup().find("p",{"class":"npws-status--closed-areas"}):
                items = wsCamping.get_soup().find("table",{"class":"itemDetails"})
                if items:
                    details = {}
                    for item in items.find_all("tr"):
                        rows = item.findChildren(['th', 'td'])
                        details[rows[0].get_text()] = rows[1].get_text().strip()
                        new_camping["details"] = details
            else:
                new_camping["status"] = "closed"
        except AttributeError as AE:
            print("Info: This camping is not available (url={})\nError: {}".format(url,AE))
            self.unavailable_campings.append(url)
            return None
        except:
            print("Fatal: something else went wrong (url={})".format(url))
            return None
        else:
            return new_camping

########################################
if __name__ == "__main__":
    print("Debug: National Parks module")


