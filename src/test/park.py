import webscrap as ws

class Park:
    def __init__(self, group=""):
        self.group = group
        self.response = ""

    def PrintPark(self):
        print(self.response)


if __name__ == "__main__":
    newPark = Park(group="")

    def GetListParks():
        NSWParks = ws.WebScraper(group="NSWNP")
        print(NSWParks.get_title)

    GetListParks()