import argparse
from bs4 import BeautifulSoup
import sys
from urllib.request import urlopen
import pickle

# parse command line args
parser = argparse.ArgumentParser(description='Curate Rotten Tomatoes ratings based on chosen critics')
parser.add_argument('critics', nargs='+',
                   help='the critics\' usernames on Rotten Tomatoes (e.g. rex-reed)')

args = parser.parse_args()
critics = args.critics

for critic in critics:
    criticUrl = "https://www.rottentomatoes.com/critic/" + critic + "/movies?page="

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
    stopPage = soup.find("section", {"class": "panel panel-rt panel-box scrollable-table"}).find(
        "ul", {"class": "pagination"}).findAll("a")[4].get("href")
    stopPageInt = int(stopPage.split("=")[1])
    counter = 0

    # assuming that only one page of reviews has been added since the last time
    if (dbExists):
        # wasteful since this should be checked earlier
        stopPageInt = 1
    # bit of a waste since the first page is captured twice
    # keep scraping until we reach the end (since RT doesn't have 404's when we hit the end)
    while (counter < stopPageInt):
        counter = counter + 1
        print("Loading " + critic + "'s review page " +
              str(counter) + " of " + str(stopPageInt) + "...")
        # might contain duplicate ratings (how to fix?)
        r = urlopen(criticUrl + str(counter)).read()
        soup2 = BeautifulSoup(r, "lxml")
        mydivs = soup2.findAll("table", {"class": "table table-striped"})
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
                        criticRatings[str(tr.find("a").contents[0])] = str(
                            rating)
                except IndexError:
                    pass
    print("Saving database...")
    pickle.dump(criticRatings, open(critic + ".pickle", "wb"))


# show user interactive prompt to search for movies and their ratings
ratings = []

for critic in critics:
    ratings.append(pickle.load(open(critic + ".pickle", "rb")))


def parseDivide(inputVal):
    inputVal = inputVal.split("/")
    numerator = inputVal[0]
    denominator = inputVal[1]
    return str(float(numerator) / float(denominator))


moviesAllReviewed = ratings[0]

counter = 1
while (counter < len(ratings)):
    moviesAllReviewed = moviesAllReviewed & ratings[counter].keys()
    counter = counter + 1

# lowercase all movies to help with searching
moviesAllReviewed = [x.lower() for x in moviesAllReviewed]

ratingsTmp = []
for rating in ratings:
    ratingsTmp.append({k.lower(): v for k, v in rating.items()})

ratings = ratingsTmp


def calculateCombinedRating(movieName):
    counter = 0
    movieName = movieName.lower()
    localRatings = []
    while (counter < len(ratings)):
        criticRating = parseDivide(ratings[counter][movieName])
        print(critics[counter] + " rated " +
              movieName + ": " + str(criticRating))
        counter = counter + 1
        localRatings.append(float(criticRating))

    combinedRating = sum(localRatings) / len(localRatings)
    print("Combined rating: " + str(round(combinedRating, 2)))


while True:
    try:
        response = input(
            "Enter a movie name (press Ctrl-C to quit; type 'show all movies' to show all movies reviewed by all critics):")
        if (response == "show all movies"):
            print(moviesAllReviewed)
        else:
            calculateCombinedRating(response)
    except KeyError:
        print("Movie was not reviewed by all critics.")
