import nationalparks as NP
import database as db

def GetCampingsDates(date):
    
    NP.GetCampingDate("https://www.nationalparks.nsw.gov.au/camping-and-accommodation/campgrounds/trial-bay-gaol-campground", date, debug=True)

if __name__ == "__main__":
    GetCampingsDates("20230412")