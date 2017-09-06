import feedparser
import pygmail
import time
import pprint


def getURLs(filename):
	with open(filename, 'r') as f:
		urls = f.readlines()
	return urls

def notify(jobs, sender, receiver):
	message = ''
	for job in jobs:
		message = message + 'Title: {}\nSummery: {}\nLink: {}\n\n'.format(job.title, job.summary, job.link)

	if message:
		pygmail.send_mail(sender, receiver, 'Upwork-Hunt Jobs', message)

def main():
	filename = input('Enter the name of file containing Atom feed URLs > ') or 'urls.txt'
	wait = int(input('Enter time to wait between scans (in seconds) > ') or 50)
	sender = input('Enter the Gmail address of the notification sender > ')
	receiver = input('Enter the receiver of the notification receiver > ')
	urls = getURLs(filename)
	feeds = [feedparser.parse(url) for url in urls]
	scraped = {}

	while True:
		tosend = []
		for url in urls:
			feed = feedparser.parse(url)

			for job in feed.entries:
				if not job.link in scraped:
					tosend.append(job)
					scraped[job.link] = True

		if tosend: 
			notify(tosend, sender, receiver)
		time.sleep(wait)

if __name__=='__main__':
	main()
	