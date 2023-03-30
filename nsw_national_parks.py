import webscrap as ws

def GetListParks(group=""):
    wsGroup = ws.WebScraper(group=group)

    if wsGroup.group == "NSWNP":
        for element in wsGroup.get_soup().find_all("li",{"class":"headingIcon icon tree visit"}):
            wsGroup.locations.append({
                "name": element.get_text().strip(),
                "url": element.a["href"].strip()
            })
    return wsGroup.locations

def GetParkInfo(url=""):
    wsPark = ws.WebScraper(url=url)
    return wsPark.get_soup().find("div",{"class":"content"}).get_text().strip()

########################################
if __name__ == "__main__":

    nswParks = GetListParks(group="NSWNP")
    print(nswParks)
