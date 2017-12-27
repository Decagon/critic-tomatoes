from bs4 import BeautifulSoup
import sys
from urllib.request import urlopen
import pickle
sys.setrecursionlimit(20000)
criticUrls = ["https://www.rottentomatoes.com/critic/rex-reed/movies", "https://www.rottentomatoes.com/critic/anthony-lane/movies"]
for criticUrl in criticUrls:
    criticUrl = criticUrl + "?page="
    critic = criticUrl.split("/")[4]

    # find the database file, if it exists
    dbExists = False
    try:
        criticRatings = pickle.load(open(critic + ".pickle", "rb"))
        dbExists = True
    except Exception:
        criticRatings = {}
        dbExists = False

    r = urlopen(criticUrl + "1").read()
    soup = BeautifulSoup(r, "lxml")

    # find how many pages this reviewer has
    stopPage = soup.find("section", {"class": "panel panel-rt panel-box scrollable-table"}).find("ul", {"class": "pagination"}).findAll("a")[4].get("href")
    stopPageInt = int(stopPage.split("=")[1])
    counter = 0

    # assuming that only one page of reviews has been added since the last time
    if (dbExists):
        # wasteful since this should be checked earlier
        stopPageInt = 1;
    # bit of a waste since the first page is captured twice
    # keep scraping until we reach the end (since RT doesn't have 404's when we hit the end)
    while (counter < stopPageInt):
        counter = counter + 1
        print("Loading " + critic + "'s review page " + str(counter) + " of " + str(stopPageInt) + "...")
        # might contain duplicate ratings (how to fix?)
        r = urlopen(criticUrl + str(counter)).read()
        soup2= BeautifulSoup(r, "lxml")
        mydivs = soup2.findAll("table", { "class" : "table table-striped" })
        for div in mydivs:
                for tr in div.findAll("tr"):
                        rating = tr.find("span")
                        if (rating is None):
                            continue

                        # sometimes there will be no rating, just a tomato or splat
                        # so give the splats a zero score, and a tomato a one
                        if (rating["title"] == ""):
                            if (rating["class"] == "icon tiny fresh"):
                                rating = "1/1"
                            else:
                                rating = "0/1"
                        else:
                            rating = rating["title"]

                        try:
                            movie = tr.find("a").contents[0]
                            if (movie is not None):
                                criticRatings[str(tr.find("a").contents[0])] = str(rating)
                        except IndexError:
                            pass
    print("Saving database...")
    pickle.dump(criticRatings, open(critic + ".pickle", "wb"))
