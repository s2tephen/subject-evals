# MIT Subject Evaluations scraper

Simple scraper for MIT Subject Evaluations built with [Mechanize](http://wwwsearch.sourceforge.net/mechanize/) and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html). Tested in Python 2.7.2.

## Setup
Clone this repo and create a file named `login.py` in your local directory. It should look like this:
```
login = {
  'username': YOUR_ATHENA_USERNAME,
  'password': YOUR_ATHENA_PASSWORD
}
```
Then, run `python scrape.py` in console with any of the following flags:
* `-t TERM` - narrows query by term, format is YYYY(FA|JA|SP|SU)
* `-d DEPT` - narrows query by department, use course number or abbreviation

If unspecified, the script will scrape all listings available on the site. These queries are additive and will stack into the same file, so you can run multiple queries for longitudinal data.
