import requests
from lxml import html

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

page = requests.get(url)
tree = html.fromstring(page.content)

scraped_jobs = tree.xpath('//section[@class="job-tile"]')
jobs = []

for job in scraped_jobs:
	job_dict = {
	'title': job.xpath('/div[0]/text()'),
	}

	jobs.append(job_dict)