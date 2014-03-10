import re, os, csv
import mechanize
from BeautifulSoup import BeautifulSoup

library = []
<<<<<<< HEAD
subjects = []
if os.path.isfile('evals.csv'):
  for r in csv.DictReader(open('evals.csv')):
    subjects.append(r['subject'])

br = mechanize.Browser()
br.addheaders = [('User-agent','Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')]
br.set_handle_robots(False)

print 'scraping...'

for s in subjects:
  print '  ' + s,
  br.open('http://student.mit.edu/catalog/search.cgi?search=' + s + '&style=verbatim')
  soup = BeautifulSoup(br.response().read())
  match = re.search('Units: [0-9]+-[0-9]+-[0-9]+', soup.find('blockquote').text)
  if match:
    subunits = match.group(0).split(':')[1].strip().split('-')
    u = sum([int(str(su)) for su in subunits])
    library.append({'subject': s, 'units': u})
    print '...ok'
  else:
    print '...not found'
    continue

print '...done!'

field_names = ['subject', 'units']
writer = csv.DictWriter(open('units.csv', 'wb'), fieldnames=field_names)
headers = dict((n, n) for n in field_names)
writer.writerow(headers)
for data in library:
  writer.writerow(data)
