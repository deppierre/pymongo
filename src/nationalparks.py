import webscraper as ws
from datetime import timedelta, date
import calendar

def GetListParks(url):
    locations = []
    soup = ws.get_soup(url)

    if soup:
        for element in soup.find_all("li",{"class":"headingIcon icon tree visit"}):
            locations.append({
                "name": element.get_text().strip(),
                "url": element.a["href"].strip(),
                "campings": []
            })
    return locations

def ParksInfo(url):
    Parks = GetListParks(url + "/conservation-and-heritage/national-parks")

    for idx, park in enumerate(Parks):
        soup = ws.get_soup(park["url"])

        for element in soup.find_all("div",{"class":"scrollingBox__item camping"}):
            Parks[idx]["campings"].append(url + element.a["href"].strip())
    
    return Parks
        
def GetCampingInfo(url="",debug=False):
    if debug: print("Debug: GetCampingInfo(url={})".format(url))
    soup = ws.get_soup(url)
    # wsCampingMap = ws(url=url+"/visitor-info")
    new_camping = {}
    # if wsCampingMap:
    #     new_camping["map_url"] = url + wsCampingMap.get_soup().find("li",{"class":"headingIcon icon pdf"}).a["href"]
    # else:
    #     new_camping["map_url"] = url + soup.find("li",{"class":"headingIcon icon pdf"}).a["href"]
    if soup:
        try:
            new_camping["name"] = soup.find("h1",{"class":"show-inline"}).get_text().strip()
            new_camping["location"] = soup.find("p",{"class":"tabbedPageSubTitle"}).get_text().strip()
            new_camping["url"] = url
            new_camping["status"] = "opened"
            if not soup.find("p",{"class":"npws-status--closed-areas"}):
                items = soup.find("table",{"class":"itemDetails"})
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
            return None
        except:
            print("Fatal: something else went wrong (url={})".format(url))
            return None
        else:
            return new_camping
        
def GetCampingDate(url, begin_date, end_date=None):

    start_date = date(int(begin_date[:4]), int(begin_date[4:6]), int(begin_date[6:8]))
    end_date = start_date + timedelta(days=1)

    _url = url + "?dateFrom={dd_from}%20{mm_from}%20{yy_from}&dateTo={dd_to}%20{mm_to}%20{yy_to}&adults=1&children=0&infants=0".format(
        dd_from = start_date.strftime("%d"),
        mm_from = calendar.month_abbr[start_date.month],
        yy_from = start_date.strftime("%Y"),
        dd_to = end_date.strftime("%d"),
        mm_to = calendar.month_abbr[end_date.month],
        yy_to = end_date.strftime("%Y")
    )
    soup = ws.get_soup(_url)

    for element in soup.find_all("div",{"id":"availability"}):
        print(element)
        # Parks[idx]["campings"].append(url + element.a["href"].strip())
    else:
        with open('failed.html', 'w') as file:
            file.write(str(soup))

########################################
if __name__ == "__main__":
    print("Debug: National Parks module")