import re, os, csv, urllib2
import mechanize
from BeautifulSoup import BeautifulSoup
from login import login

# set basic parameters
TARGET_URL = 'https://edu-apps.mit.edu/ose-rpt'

# login with kerberos
br = mechanize.Browser()
br.addheaders = [('User-agent','Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')]
br.set_handle_robots(False)
br.open(TARGET_URL)
br.select_form(nr=1)
br.form['j_username'] = login['username']
br.form['j_password'] = login['password']
br.submit()
br.select_form(nr=0)
br.submit()

# search all the things
br.open('subjectEvaluationSearch.htm?termId=&departmentId=&subjectCode=*&instructorName=&search=Search')
indexSoup = BeautifulSoup(br.response().read())
links = indexSoup.findAll('a')[3:]
for l in links:
  br.open(l.get('href'))
  linkSoup = BeautifulSoup(br.response().read())
  crossListings = len(soup.findAll('h1')[2].findAll('br'))

# send request and soupify
# request = urllib2.Request(TARGET_URL, None, HEADERS)
# response = urllib2.urlopen(request)
# soup = BeautifulSoup(response)

# structure dat data
# print 'scraping...'
# links = soup.findAll('td', 'title')[1::2]
# for l in links:
#   id_ = l.parent.nextSibling.findAll('a')[1].get('href').split('=')[1]
#   if id_ not in ids:
#     data = {}
#     data['id'] = l.parent.nextSibling.findAll('a')[1].get('href').split('=')[1]
#     data['url'] = l.a.get('href')
#     data['title'] = l.a.text
#     data['user'] = l.parent.nextSibling.findAll('a')[0].text
#     data['comments'] = l.parent.nextSibling.findAll('a')[1].text.split(' ')[0]
#     link_list.append(data)
#   else: # only update comment count if already in db
#     data = link_list[ids.index(id_)]
#     data['comments'] = l.parent.nextSibling.findAll('a')[1].text.split(' ')[0]
#   print '  ' + l.a.get('href')
# print '...done!'

# output to csv
# field_names = link_list[0].keys()
# writer = csv.DictWriter(open('hacker_news.csv', 'wb'), fieldnames=field_names)
# headers = dict((n, n) for n in field_names)
# writer.writerow(headers)
# for data in link_list:
#   if data in ids:
#     writer.writerow(data)
#   else:
#     writer.writerow(dict((k, v.encode('utf8')) for k, v in data.iteritems()))
