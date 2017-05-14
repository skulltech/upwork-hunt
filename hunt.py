import requests
import wdstart

from lxml import html
from selenium import webdriver


urls = {
	'web-soft-dev': 'https://www.upwork.com/o/jobs/browse/c/web-mobile-software-dev/',
	'it-networking': 'https://www.upwork.com/o/jobs/browse/c/it-networking/',
	'data-sci': 'https://www.upwork.com/o/jobs/browse/c/data-science-analytics/',
	'engg-arch': 'https://www.upwork.com/o/jobs/browse/c/engineering-architecture/',
	'design': 'https://www.upwork.com/o/jobs/browse/c/design-creative/',
	'writing': 'https://www.upwork.com/o/jobs/browse/c/writing/',
	'translation': 'https://www.upwork.com/o/jobs/browse/c/translation/',
	'legal': 'https://www.upwork.com/o/jobs/browse/c/legal/',
	'admin-support': 'https://www.upwork.com/o/jobs/browse/c/admin-support/',
	'customer-service': 'https://www.upwork.com/o/jobs/browse/c/customer-service/',
	'sales-market': 'https://www.upwork.com/o/jobs/browse/c/sales-marketing/',
	'account-consulting': 'https://www.upwork.com/o/jobs/browse/c/accounting-consulting/'
}

url = urls['it-networking']


browser = wdstart.start_webdriver('Chrome')
browser.get(url)

'''
page = requests.get(url)
tree = html.fromstring(page.content)
'''

scraped_jobs = browser.find_elements_by_class_name('job-tile')[:10]
jobs = []

for job in scraped_jobs:
	job_dict = {
	'id': job.get_attribute('id')[4:],
	'link': 'https://www.upwork.com/o/jobs/job/_' + job.get_attribute('id')[4:],
	'title': job.find_element_by_tag_name('h2').text,
	'description': job.find_elements_by_tag_name('span')[6].get_attribute('textContent')
	}

	jobs.append(job_dict)

print(jobs)