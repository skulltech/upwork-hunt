import feedparser
import pygmail
import time
import pprint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


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

def login(username, password, driver):
	driver.get('https://www.upwork.com/ab/account-security/login')
	driver.find_element_by_id('login_username').send_keys(username)
	passfield = driver.find_element_by_id('login_password')
	passfield.send_keys(password)
	passfield.submit()

def send_proposal(link, driver, proposal):
	jobID = link[-29:-11]
	driver.get('https://www.upwork.com/ab/proposals/job/~{}/apply/'.format(jobID))
	try:
		duration = driver.find_element_by_id('apply_duration')
	except NoSuchElementException:
		pass
	else:
		duration.click()
		duration.find_element_by_xpath('/div/ul/li[2]').click()

	additional = driver.find_element_by_css_selector('div.air-card')
	for textarea in additional.find_element_by_css_selector('textarea'):
		textarea.send_keys(proposal)

	driver.find_element_by_xpath('a[@data-olog-name="apply"]').click()

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
	