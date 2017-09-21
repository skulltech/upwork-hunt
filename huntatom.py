import feedparser
import pygmail
import time
import pprint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
	passfield = driver.find_element_by_id('login_password').send_keys(password)
	driver.find_element_by_xpath('//button[@type="submit"]').click()

def send_proposal(jobID, driver, proposal):
	driver.get('https://www.upwork.com/ab/proposals/job/~{}/apply/'.format(jobID))
	time.sleep(5)

	try:
		driver.find_elements_by_css_selector('span.checkbox-replacement-helper')[1].click()
	except (NoSuchElementException, IndexError):
		pass

	try:
		duration = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'apply_duration')))
	except NoSuchElementException:
		pass
	else:
		driver.execute_script("arguments[0].scrollIntoView();", duration)
		duration.find_element_by_css_selector('div.btn-group.dropdown').click()
		driver.find_elements_by_css_selector('.eo-dropdown-menu > li')[1].click()

	driver.find_element_by_id('coverLetter').send_keys(proposal)
	i = 1
	while (i > 0):
		try:
			driver.find_element_by_id('question{}'.format(i)).send_keys(proposal)
		except NoSuchElementException:
			break
		else:
			i = i+1

	driver.find_elements_by_css_selector('a.m-0')[0].click()
	time.sleep(5)
	try:
		driver.find_element_by_css_selector('div.modal-body > div.checkbox').click()
		driver.find_element_by_css_selector('button.btn.btn-primary').click()
	except NoSuchElementException:
		pass

def main():
	filename = input('Enter the name of file containing Atom feed URLs > ') or 'urls.txt'
	wait = int(input('Enter time to wait between scans (in seconds) > ') or 50)
	sender = input('Enter the Gmail address of the notification sender > ')
	receiver = input('Enter the receiver of the notification receiver > ')
	username = input('Enter your Upwork username > ')
	password = input('Enter your Upwork password > ')
	proposal = input('Enter your Upwork proposal > ')

	driver = webdriver.Firefox()
	login(username, password, driver)
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
			jobID = link[-29:-11]
			send_proposal(jobID, driver, proposal)
		time.sleep(wait)

if __name__=='__main__':
	main()
	
