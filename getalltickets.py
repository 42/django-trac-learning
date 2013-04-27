import urllib2

url = 'https://code.djangoproject.com/query?format=csv&col=id&col=time' \
    + '&col=changetime&col=reporter&col=summary&col=status&col=owner&col=type' \
    + '&col=component&order=priority' 
tickets = urllib2.urlopen(url).read()

open('2013-04-27.csv','w').write(tickets)
