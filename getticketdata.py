from bs4 import BeautifulSoup
import csv
import datetime
import urllib2
import urlparse

def get_data(ticket):
    try:
        url = 'https://code.djangoproject.com/ticket/%s' % ticket
        ticket_html = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print 'Failed to get "%s"' % url
        return
    bs = BeautifulSoup(ticket_html)
    
    # get closing date
    d = bs.find_all('div','date')[0]
    try: 
        p = list(d.children)[3]
    except IndexError: 
        print d
        return
    href = p.find('a')['href']
    close_time_str = urlparse.parse_qs(href)['/timeline?from'][0]
    close_time = datetime.datetime.strptime(close_time_str[:-6], 
                                            '%Y-%m-%dT%H:%M:%S')
    tz_hours = int(close_time_str[-5:-3])
    tz_minutes = int(close_time_str[-2:])
    if close_time_str[-6]=='-':
        tz_hours = -tz_hours
    close_time -= datetime.timedelta(hours = tz_hours, minutes = tz_minutes)

    # get description and return
    de = bs.find_all('div', 'description')[0]
    return close_time, de.text

tickets_file = csv.reader(open('2013-04-27.csv'))
output = csv.writer(open('2013-04-27.close.csv','w'))

tickets_file.next()
for id, time, changetime, reporter, summary, status, owner, type, component \
        in tickets_file:
    try:
        closetime, descr = get_data(id)
    except: 
        continue
    if closetime is None: continue
    row = [id]
    row.extend([time,
                changetime,
                closetime,
                reporter,
                summary,
                status,
                owner,
                type,
                component,
                descr.encode('utf-8'),
                ],
               )
    output.writerow(row)
    print id, closetime
