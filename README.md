# critic-tomatoes
Curated Rotten Tomatoes ratings based on chosen critics. Open up critic-tomoatoes.py and add/change the urls of your critics, then run the script with `python3 critic-tomatoes.py`. This will create a database of ratings for each of your critics. To update the database, just run `python3 critic-tomatoes.py` and it will fetch the first page of ratings and add it to the pre-existing database. 

The code is very low quality right now. Run `python3 reader.py` after generating the database (and make sure to change the filenames in `reader.py`) to show an average rating of each of the movies that both critics reviewed.

## Sample Output

```
De rouille et d'os (Rust and Bone): 0.0%
Jersey Boys: 75.0%
The Kids Are All Right: 75.0%
Nancy Drew: 0.0%
The Danish Girl: 100.0%
Blue Valentine: 0.0%
The Shape of Water: 25.0%
Birdman: 25.0%
Mission: Impossible III: 0.0%
Logan Lucky: 25.0%
The Humbling: 25.0%
The Two Faces of January: 70.0%
Albert Nobbs: 50.0%
The Best of Youth (La meglio gioventù): 0.0%
```

Inspired by this Reddit thread: https://www.reddit.com/r/Lightbulb/comments/7lywl1/the_ability_to_favorite_or_subscribe_to_reviewers/
