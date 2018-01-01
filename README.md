# critic-tomatoes
Curated Rotten Tomatoes ratings based on chosen critics.

[![Updates](https://pyup.io/repos/github/Decagon/critic-tomatoes/shield.svg)](https://pyup.io/repos/github/Decagon/critic-tomatoes/) [![Python 3](https://pyup.io/repos/github/Decagon/critic-tomatoes/python-3-shield.svg)](https://pyup.io/repos/github/Decagon/critic-tomatoes/)


```
usage: critic-tomatoes.py [-h] critics [critics ...]

Curate Rotten Tomatoes ratings based on chosen critics

positional arguments:
  critics     the critics' usernames on Rotten Tomatoes (e.g. rex-reed)

optional arguments:
  -h, --help  show this help message and exit
```

## Sample usage

To search for curated ratings for `rex-reed` and `anthony-lane` (those Rotten Tomatoes's critics), run `python3 critic-tomatoes.py rex-reed anthony-lane`. After the database file has been downloaded, you will recieve a prompt to enter in a movie name. Type in a movie name, press enter, and it will show the curated rating from each critic, and the combined rating. Want more critics? Add as many as you'd like.

```
decagon@server:~$ python3 critic-tomatoes.py rex-reed anthony-lane
Loading rex-reed's review page 1 of 1...
Saving database...
Loading anthony-lane's review page 1 of 1...
Saving database...
Enter a movie name (press Ctrl-C to quit; type 'show all movies' to show all movies reviewed by all critics): insomnia
rex-reed rated insomnia: 0.0
anthony-lane rated insomnia: 0.0
Combined rating: 0.0
```

Inspired by this Reddit thread: https://www.reddit.com/r/Lightbulb/comments/7lywl1/the_ability_to_favorite_or_subscribe_to_reviewers/
