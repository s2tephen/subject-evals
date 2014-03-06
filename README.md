# MIT Subject Evaluations scraper

Simple scraper for MIT Subject Evaluations listings built with Mechanize and BeautifulSoup.

## Setup
Clone this repo and create a file named `login.py` in your local directory. It should look like this:
```
login = {
  'username': YOUR_USERNAME,
  'password': YOUR_PASSWORD
}
```
In `scrape.py`, narrow your scope in the variables section at the top (by default, it will scrape everything). Then, run `python scrape.py` in console.
