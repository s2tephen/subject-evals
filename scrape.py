import re, os, csv, urllib2
import mechanize
from BeautifulSoup import BeautifulSoup
from login import login
from optparse import OptionParser

# initialize variables
parser = OptionParser()
parser.add_option('-t', '--term', dest='term', default='', help='format: YYYY(FA|JA|SP|SU)', metavar='TERM')
parser.add_option('-d', '--dept', dest='dept', default='', help='course # or abbreviation', metavar='DEPT')

(options, args) = parser.parse_args()
library = []
cached_keys = []
if options.dept != '':
  for i in range(0, 4 - len(options.dept)):
    options.dept = '+' + options.dept

if os.path.isfile('evals.csv'):
  for r in csv.DictReader(open('evals.csv')):
    cached_keys.append(r['url'])
    library.append(r)

# setup browser
br = mechanize.Browser()
br.addheaders = [('User-agent','Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')]
br.set_handle_robots(False)

# login with kerberos
br.open('https://edu-apps.mit.edu/ose-rpt')
br.select_form(nr=1)
br.form['j_username'] = login['username']
br.form['j_password'] = login['password']
br.submit()
br.select_form(nr=0)
br.submit()

# search all the things
br.open('subjectEvaluationSearch.htm?termId=' + options.term + '&departmentId=' + options.dept + '&subjectCode=*&instructorName=&search=Search')
index_soup = BeautifulSoup(br.response().read())
links = index_soup.findAll('a')[3:]

# build records
print 'scraping...'
for l in links:
  href = l.get('href')
  if l.get('href') not in cached_keys:
    br.open(href)
    link_soup = BeautifulSoup(br.response().read())

    # initialize variables
    data = {}
    questions, avgs, responses, stddevs = [], [], [], []

    # scrape summary data
    data['subject'] = link_soup.findAll('h1')[2].contents[0].strip().split('&nbsp;')[0]
    data['full_name'] = link_soup.findAll('h1')[2].contents[0].strip().split('&nbsp;')[1]
    data['term'] = re.search('(Fall|January|Spring|Summer) [0-9]{4}', link_soup.findAll('h2')[0].contents[0]).group(0)
    print '  ' + data['subject'] + ', ' + data['term'],
    summary_data = link_soup.findAll('p', 'tooltip')
    data['eligible'] = str(summary_data[0].contents[1]).split()
    data['respondents'] = str(summary_data[1].contents[1]).split()
    data['response_rate'] = str(summary_data[2].contents[1]).split()

    # scrape subject data
    subject_data = link_soup.findAll('table', 'indivQuestions')[0:3] # ignore extra tables, e.g. HKN data
    for section in subject_data:
      questions += [td.text for td in section.findAll('td', {'width': 300})]
      avgs += [td.text for td in section.findAll('td', {'width': '35px'})]
      responses += [td.text for td in section.findAll('td', {'width': 75})]
      stddevs += [td.text for td in section.findAll('td', {'width': 50})]
    for i in range(0, len(questions) - 1):
      data['q' + str(i + 1)] = questions[i]
      data['avg' + str(i + 1)] = avgs[i]
      data['n' + str(i + 1)] = responses[i]
      data['sd' + str(i + 1)] = stddevs[i]

    data['url'] = href
    library.append(data)
    print ' ...ok'
print '...done!'

# output to csv
field_names = library[0].keys()
writer = csv.DictWriter(open('evals.csv', 'wb'), fieldnames=field_names)
headers = dict((n, n) for n in field_names)
writer.writerow(headers)
for data in library:
  writer.writerow(data)
