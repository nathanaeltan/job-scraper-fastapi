import requests
from bs4 import BeautifulSoup
import random


def format_job_title(job_title: str):
    return job_title.strip().replace(" ", "+")


class JobScraper:
    def __init__(self, job_title):
        self.title = format_job_title(job_title)

    async def scrape_jobs(self):
        node_flair_data = await self._scrape_nodeflair()
        job_db_data = await self._scrape_jobs_db()
        job_street_data = await self._scrape_jobstreet()
        combined_list = node_flair_data + job_db_data + job_street_data
        random.shuffle(combined_list)
        return combined_list

    async def _scrape_jobs_db(self):
        url = f"https://sg.jobsdb.com/j?sp=homepage&trigger_source=homepage&q={self.title}&l="
        headers = requests.utils.default_headers()
        headers.update({
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        })

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        job_cards = soup.find_all("div", {'class': ['job-card', 'result']})
        job_data = []
        for job_card in job_cards:
            job_card_a = job_card.find('a')
            title = job_card_a.text
            href_value = "https://sg.jobsdb.com" + job_card_a.get("href")
            company = job_card.find(class_='job-company').text
            job_data.append({
                'title': title,
                'company': company,
                'source': 'JobsDB',
                'link': href_value
            })
        return job_data

    async def _scrape_jobstreet(self):
        url = f"https://www.jobstreet.com.sg/{self.title.replace('+', '-')}-jobs"
        headers = requests.utils.default_headers()
        headers.update({
            'Accept': '*/*',
            'Accept-Language': 'een-GB,en;q=0.7',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        })
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        job_cards = soup.find_all('article', {'data-card-type': 'JobCard'})
        job_data = []
        for job_card in job_cards:
            job_card_a = job_card.find('a')
            href_value = "https://www.jobstreet.com.sg" + job_card_a.get('href')
            all_anchor = job_card.find_all('a')
            title = all_anchor[1].text
            company = all_anchor[2].text
            job_data.append({
                'title': title,
                'company': company,
                'source': 'JobStreet',
                'link': href_value
            })
        return job_data

    async def _scrape_nodeflair(self):
        url = f"https://nodeflair.com/api/v2/jobs?query={self.title}&page=1&sort_by=relevant"
        headers = requests.utils.default_headers()
        headers.update({
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Referer': 'https://nodeflair.com/jobs?query=software',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'X-Requested-With': 'Fetch'
        })
        response = requests.get(url, headers=headers)

        data = response.json()
        job_listings = data['job_listings']
        job_data = []
        for job in job_listings:
            job_data.append({
                'title': job['title'],
                'company': job['company']['companyname'],
                'source': 'NodeFlair',
                'link': 'https://nodeflair.com/' + job['job_path']
            })

        return job_data
