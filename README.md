# critic-tomatoes
Curated Rotten Tomatoes ratings based on chosen critics. Open up critic-tomoatoes.py and add/change the urls of your critics, then run the script with `python3 critic-tomatoes.py`. This will create a database of ratings for each of your critics. To update the database, just run `python3 critic-tomatoes.py` and it will fetch the first page of ratings and add it to the pre-existing database.

The code is very low quality right now. Run `python3 reader.py` after generating the database (and make sure to change the filenames in `reader.py`) to show an average rating of each of the movies that both critics reviewed.
