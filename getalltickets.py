import urllib2

url = 'https://code.djangoproject.com/query?format=csv&col=id&col=time' \
    + '&col=changetime&col=reporter&col=summary&col=status&col=owner&col=type' \
    + '&col=component&order=priority' 
tickets = urllib2.urlopen(url).read()

open('2012-10-09.csv','w').write(tickets)
