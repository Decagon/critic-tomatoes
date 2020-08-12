import argparse
import urllib.request

from bs4 import BeautifulSoup
import stringcase


def __main__():
    # parse command line args
    parser = argparse.ArgumentParser(description='Curate Rotten Tomatoes ratings based on chosen critics')
    parser.add_argument('critics', nargs='+',
                        help='the critics\' usernames on Rotten Tomatoes (e.g. rex-reed)')

    args = parser.parse_args()
    critics = args.critics
    critic_reviews = {}
    for critic in critics:
        critic_reviews[critic] = get_critic_reviews(critic)

    while True:
        query = input("What is the title of the movie? (press Ctrl+C to quit) ")
        for reviewer in critic_reviews.keys():
            reviews = critic_reviews[reviewer]
            for review in reviews:
                title = review[1]
                score = review[0]
                if query.lower().strip() in title.lower():
                    print(f"{reviewer} rated {stringcase.titlecase(title)} a score of {score*100}%")


def get_critic_reviews(critic):
    """
    Downloads reviews for a critic
    :param critic: The critic to get reviews from
    """
    critic_url: str = f"https://www.rottentomatoes.com/critic/{critic}/movies?page="
    reviews = []
    page: int = 1
    while True:
        print(f"Downloading page {page}...")
        review_html = urllib.request.urlopen(critic_url + str(page)).read()
        review_page = download_reviews(review_html)
        if len(review_page) == 0:
            break
        reviews.extend(review_page)
        page += 1
    return reviews


def get_review_score(review):
    """
    Parses a n/p review into a float
    :param review: The review to parse
    :return: A float representing the fractional review score
    """
    score = review.find("td").text.strip()
    if len(score) != 0:
        try:
            return int(score.split("/")[0]) / float(score.split("/")[1])
        except ValueError:
            return 0
    else:
        return 1 if 'fresh' in review.find("td").find("span").get('class') else 0


def download_reviews(r):
    """
    Returns a list of reviews for a page (score and link)
    :param r: The review html to parse
    :return: A score and link for each review
    """
    soup = BeautifulSoup(r, "lxml")
    review_bodies = soup.find("tbody", {"id": "review-table-body"})
    reviews = review_bodies.find_all("tr")
    completed_reviews = []
    if len(reviews) == 0:
        return []
    for review in reviews:
        score = get_review_score(review)
        link = review.find("a").get('href')
        title = link.split('/')[-1].replace('_', ' ')
        completed_reviews.append((score, title, link))
    return completed_reviews


__main__()
