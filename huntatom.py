import feedparser
import pygmail
import time


ATOMURL = 'https://www.upwork.com/ab/feed/jobs/atom?sort=renew_time_int+desc&api_params=1&q=&securityToken=01e854aff6edad8f9d09dfb1eed5f0237a06f558faad4c34cf0583e91ad88e6f34cea3e91acc650a75b64528f47070829bbc701fc57b5e9799219bd037f7778b&userUid=516618899203964928&orgUid=516618899212353537'
feed = feedparser.parse(ATOMURL)

def getURLs(filename):
	with open(filename, 'r') as f:
		urls = f.readlines()
	return urls

def notify(job, sender, receiver):
	messagedict = {
		'Title': job.title,
		'Summary': job.summary,
		'Link': job.link 
	}
	message = pprint.pformat(messagedict)
	pygmail.send_mail(sender, receiver, 'Upwork-Hunt Job: {}'.format(messagedict['Title']), message)


filename = input('Enter the name of file containing Atom feed URLs > ') or 'urls.txt'
wait = int(input('Enter time to wait between scans (in seconds) > ')) or 50
urls = getURLs(filename)
feeds = [feedparser.parse(url) for url in urls]
scraped = {}

while True:
	for url in urls:
		feed = feedparser.parse(url)

		for job in feed.entries:
			if not job.link in scraped:
				notify(job)
				scraped[job.link] = True
	time.sleep(wait)