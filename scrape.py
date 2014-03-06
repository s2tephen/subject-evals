import re, os, csv
import mechanize
from BeautifulSoup import BeautifulSoup
from login import login
from optparse import OptionParser

# initialize variables
parser = OptionParser()
parser.add_option('-t', '--term', dest='term', default='', help='format: YYYY(FA|JA|SP|SU)', metavar='TERM')
parser.add_option('-d', '--dept', dest='dept', default='', help='course # or abbreviation', metavar='DEPT')

(options, args) = parser.parse_args()
library, cached_keys, temp_cache = [], [], []
max_questions = 0
if options.dept != '':
  for i in range(0, 4 - len(options.dept)):
    options.dept = '+' + options.dept

if os.path.isfile('evals.csv'):
  for r in csv.DictReader(open('evals.csv')):
    cached_keys.append(r['url'])
    max_questions = max(max_questions, int(r['questions']))
    library.append(r)

# setup browser
br = mechanize.Browser()
br.addheaders = [('User-agent','Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')]
br.set_handle_robots(False)

# login with athena
br.open('https://edu-apps.mit.edu/ose-rpt')
br.select_form(nr=1)
br.form['j_username'] = login['username']
br.form['j_password'] = login['password']
br.submit()
br.select_form(nr=0)
br.submit()

# search all the things
br.open('subjectEvaluationSearch.htm?termId=' + options.term + '&departmentId=' + options.dept + '&subjectCode=4.140&instructorName=&search=Search')
index_soup = BeautifulSoup(br.response().read())
links = index_soup.findAll('a')[3:]

# build records
print 'scraping...'
for l in links:
  href = l.get('href')
  if href not in cached_keys:
    temp_cache.append(href)
    br.open(href)
    link_soup = BeautifulSoup(br.response().read())

    # initialize variables
    data = {}
    questions, avgs, responses, stddevs = [], [], [], []

    # scrape summary data
    data['subject'] = link_soup.findAll('h1')[2].contents[0::2][0:-1][temp_cache.count(href) - 1].strip().split('&nbsp;')[0]
    data['full_name'] = link_soup.findAll('h1')[2].contents[0].strip().split('&nbsp;')[1]
    data['term'] = re.search('(Fall|IAP|Spring|Summer) [0-9]{4}', link_soup.findAll('h2')[0].contents[0]).group(0)
    print '  ' + data['subject'] + ', ' + data['term'],
    summary_data = link_soup.findAll('p', 'tooltip')
    data['eligible'] = str(summary_data[0].contents[1]).strip()
    data['respondents'] = str(summary_data[1].contents[1]).strip()
    data['response_rate'] = str(summary_data[2].contents[1]).strip()

    # scrape subject data
    subject_data = link_soup.findAll('table', 'indivQuestions')
    if re.search('HKN Underground Guide', str(subject_data[-1].contents[1])):
      subject_data = subject_data[0:-1] # exclude HKN table
    for section in subject_data:
      questions += [td.text for td in section.findAll('td', {'width': 300})]
      avgs += [td.text for td in section.findAll('td', {'width': '35px'})]
      responses += [td.text for td in section.findAll('td', {'width': 75})]
      stddevs += [td.text for td in section.findAll('td', {'width': 50})]
    data['questions'] = len(questions)
    max_questions = max(max_questions, data['questions'])
    for i in range(0, data['questions'] - 1):
      data['q' + str(i + 1)] = questions[i]
      data['avg' + str(i + 1)] = avgs[i]
      data['n' + str(i + 1)] = responses[i]
      data['sd' + str(i + 1)] = stddevs[i]

    data['url'] = href
    library.append(data)
    print ' ...ok'
print '...done!'

# output to csv
field_names = ['subject', 'full_name', 'term', 'eligible', 'respondents', 'response_rate', 'questions', 'url']
for i in range(1, max_questions):
  field_names.append('q' + str(i))
  field_names.append('avg' + str(i))
  field_names.append('n' + str(i))
  field_names.append('sd' + str(i))
writer = csv.DictWriter(open('evals.csv', 'wb'), fieldnames=field_names)
headers = dict((n, n) for n in field_names)
writer.writerow(headers)
for data in library:
  writer.writerow(data)
