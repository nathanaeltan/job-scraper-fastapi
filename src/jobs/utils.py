import requests
from bs4 import BeautifulSoup


async def scrape_nodeflair(job_title):
    # url = f"https://www.nodeflair.com/jobs?query={job_title}"
    url = "https://nodeflair.com/api/v2/jobs?query=software&page=1&sort_by=relevant"
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

    # Extract and process the desired data


async def scrape_jobs_db():
    url = "https://sg.jobsdb.com/j?sp=homepage&trigger_source=homepage&q=Software+Engineer&l="
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
