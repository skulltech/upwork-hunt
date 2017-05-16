import time
import requests
import wdstart
import pygmail

from lxml import html
from selenium import webdriver


class UpworkHunt:
    def __init__(self, patterns, sender, receiver):

        self.urls = [
            'https://www.upwork.com/o/jobs/browse/c/web-mobile-software-dev/',
            'https://www.upwork.com/o/jobs/browse/c/it-networking/',
            'https://www.upwork.com/o/jobs/browse/c/data-science-analytics/',
            'https://www.upwork.com/o/jobs/browse/c/engineering-architecture/',
            'https://www.upwork.com/o/jobs/browse/c/design-creative/',
            'https://www.upwork.com/o/jobs/browse/c/writing/',
            'https://www.upwork.com/o/jobs/browse/c/translation/',
            'https://www.upwork.com/o/jobs/browse/c/legal/',
            'https://www.upwork.com/o/jobs/browse/c/admin-support/',
            'https://www.upwork.com/o/jobs/browse/c/customer-service/',
            'https://www.upwork.com/o/jobs/browse/c/sales-marketing/',
            'https://www.upwork.com/o/jobs/browse/c/accounting-consulting/'
        ]
        self.patterns = patterns
        self.filtered_jobs = []
        self.sender_email = sender
        self.receiver_email = receiver

    def scrape_jobs(self):
        jobs = []

        for url in self.urls:
            self.browser = wdstart.start_webdriver('Chrome')
            self.browser.get(url)
            scraped_jobs = self.browser.find_elements_by_class_name('job-tile')[:10]

            for job in scraped_jobs:
                job_dict = {
                    'id': job.get_attribute('id')[4:],
                    'url': 'https://www.upwork.com/o/jobs/job/_' + job.get_attribute('id')[4:],
                    'title': job.find_element_by_tag_name('h2').text,
                    'description': job.find_elements_by_tag_name('span')[6].get_attribute('textContent')
                }

                jobs.append(job_dict)

            self.browser.quit()

        return jobs

    def filter_jobs(self, jobs):
        filtered = []

        for job in jobs:
            title = job['title'].lower()
            desc = job['description'].lower()

            for pattern in self.patterns:
                if (pattern.lower() in title) or (pattern.lower() in desc):
                    filtered.append(job)
                    break

        return filtered

    def execute(self):
        scraped_jobs = self.scrape_jobs()
        jobs = self.filter_jobs(scraped_jobs)

        for job in jobs:
            if not job['id'] in self.filtered_jobs:
                self.filtered_jobs.append(job['id'])

                message = 'Title: {}\nDescription: {}\nURL: {}'.format(job['title'], job['description'], job['url'])
                pygmail.send_mail(self.sender_email, self.receiver_email, 'Upwork-Hunt Jobs', message)


def main():
    patterns = input('Enter the pattern strings to search for, seperated by comma: > ').split(',')
    sender = input('Enter the sender email address [Gmail]: > ')
    receiver = input('Enter the receiver email address: > ')

    hunter = UpworkHunt(patterns, sender, receiver)

    while True:
        hunter.execute()
        time.sleep(200)


if __name__ == '__main__':
    main()
