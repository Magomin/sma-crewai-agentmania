import json
import random
import time
from typing import List, Union, Dict
from pydantic import BaseModel
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from crewai_tools import tool
import os


class LinkedinScraperScript:
        selecting_profil = []
        accounts = {
            "dominguez.matthieu.b@gmail.com": "Stagefribl2024",
           #"matthieu@fribl.co": 'Stagefribl2024',
        }
        proxies = []

        def __init__(self):
            self.used_accounts = []
            self.cookies_dict = {}

        def select_random_account(self):
            available_accounts = [acc for acc in self.accounts.keys() if acc not in self.used_accounts]
            if not available_accounts:
                print("Error: All accounts have been used.")
                return None
            random_account = random.choice(available_accounts)
            self.used_accounts.append(random_account)  # Mark account as used
            return random_account

        def rand_proxy(self):
            proxy = random.choice(self.proxies) if self.proxies else None
            return proxy

        def login_to_linkedin(self, use_proxy=True):
            selected_account = self.select_random_account()
            if selected_account is None:
                print("No available accounts.")
                return None

            password = self.accounts[selected_account]
            proxy = self.rand_proxy() if use_proxy else None

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument("start-maximized")

            if use_proxy and proxy:
                chrome_options.add_argument(f'--proxy-server={proxy}')

            driver = webdriver.Chrome(options=chrome_options)

            driver.get("https://www.linkedin.com/login")

            email_field = driver.find_element(By.ID, 'username')
            email_field.send_keys(selected_account)
            sleep(3)

            password_field = driver.find_element(By.ID, 'password')
            password_field.send_keys(password)
            print(f"Sending password: {password}")
            sleep(5)

            login_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
            login_button.click()
            sleep(3)

            while True:
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="global-nav-typeahead"]/input')))
                    print(f"Successfully logged in {selected_account}")
                    return driver
                except TimeoutException:
                    print('Difficulty logging in, please check if captcha verification is needed')


        def scrape_profiles(self, driver, urls):
            start_time = time.time()

            class ProfileData(BaseModel):
                name: str
                job: str
                location: str
                skills: List[str]
                experience: List[str]
                certifications: List[str]
                languages: List[str]
                recommendations: List[str]
                courses: List[str]
                organizations: List[str]
                volunteering: List[str]
                activity: List[str]
                comments: List[str]

            output_data_py = []

            for page_inside in urls:
                sleep(2)
                driver.get(page_inside)
                page_source = BeautifulSoup(driver.page_source, 'html.parser')

                info_div = page_source.find('div', class_='mt2 relative')
                name = page_source.find('h1').get_text()
                job = page_source.find('div', class_="text-body-medium break-words").get_text().strip()
                location = info_div.find('span', class_="text-body-small inline t-black--light break-words").get_text().strip()

                # Skills Section
                skillpagecut = (page_inside.split('?')[0]) + '/details/skills'
                driver.get(skillpagecut)
                sleep(3)
                skillpagecut = BeautifulSoup(driver.page_source, 'html.parser')
                skill_div = skillpagecut.find('div', class_="scaffold-finite-scroll__content")
                captured_span = skill_div.find_all('span', attrs={'visually-hidden'})

                # Experience Section
                experiencepagecut = (page_inside.split('?')[0]) + '/details/experience'
                driver.get(experiencepagecut)
                sleep(3)
                experiencepagecut = BeautifulSoup(driver.page_source, 'html.parser')
                experience_div = experiencepagecut.find('div', class_="scaffold-finite-scroll__content")
                captured_span = experience_div.find_all('span', attrs={'visually-hidden'})

                # Certification Section
                certifiactionpagecut = (page_inside.split('?')[0]) + '/details/certifications'
                driver.get(certifiactionpagecut)
                sleep(3)
                certifiactionpagecut = BeautifulSoup(driver.page_source, 'html.parser')
                certification_div = certifiactionpagecut.find('div', class_="scaffold-finite-scroll__content")
                certification_span = certification_div.find_all('span', attrs={'visually-hidden'})

                # Language Section
                languagepagecut = (page_inside.split('?')[0]) + '/details/languages'
                driver.get(languagepagecut)
                sleep(3)
                languagepagecut = BeautifulSoup(driver.page_source, 'html.parser')
                language_div = languagepagecut.find('div', class_="scaffold-finite-scroll__content")
                language_span = language_div.find_all('span', attrs={'visually-hidden'})

                # Recommendations Section
                recommendationpagecut = (page_inside.split('?')[0] + '/details/recommendations')
                driver.get(recommendationpagecut)
                sleep(3)
                recommendationpagecut = BeautifulSoup(driver.page_source, 'html.parser')
                recommendation_div = recommendationpagecut.find('div', class_="scaffold-finite-scroll__content")
                recommendation_span = recommendation_div.find_all('span', attrs={'visually-hidden'})

                # Course Section
                coursepagecut = (page_inside.split('?')[0] + '/details/courses')
                driver.get(coursepagecut)
                sleep(3)
                coursepagecut = BeautifulSoup(driver.page_source, 'html.parser')
                course_div = coursepagecut.find('div', class_="scaffold-finite-scroll__content")
                course_span = course_div.find_all('span', attrs={'visually-hidden'})

                # Organizations Section
                organisationpagecut = (page_inside.split('?')[0] + '/details/courses')
                driver.get(organisationpagecut)
                sleep(3)
                organisationpagecut = BeautifulSoup(driver.page_source, 'html.parser')
                organisation_div = organisationpagecut.find('div', class_="scaffold-finite-scroll__content")
                organisation_span = organisation_div.find_all('span', attrs={'visually-hidden'})

                # Volunteering Section
                volunteringpagecut = (page_inside.split('?')[0] + '/details/voluntering-experiences')
                driver.get(volunteringpagecut)
                sleep(3)
                volunteringpagecut = BeautifulSoup(driver.page_source, 'html.parser')
                voluntering_div = volunteringpagecut.find('div', class_="scaffold-finite-scroll__content")
                voluntering_span = voluntering_div.find_all('span', attrs={'visually-hidden'})

                # Activity Section
                activitypagecut = (page_inside.split('?')[0] + '/recent-activity/all')
                driver.get(activitypagecut)
                sleep(3)
                activitypagecut = BeautifulSoup(driver.page_source, 'html.parser')
                activity_div = activitypagecut.find('ul', class_='display-flex flex-wrap list-style-none justify-center')
                if activity_div:
                    activity_span = activity_div.find_all('span', dir={'ltr'})[:100]
                else:
                    activity_span = []

                # Comments Section
                commentpagecut = (page_inside.split('?')[0] + '/recent-activity/comments/')
                driver.get(commentpagecut)
                sleep(3)
                commentpagecut = BeautifulSoup(driver.page_source, 'html.parser')
                comment_div = commentpagecut.find('ul', class_='display-flex flex-wrap list-style-none justify-center')
                if comment_div:
                    comment_span = comment_div.find_all('span', dir={'ltr'})[:100]
                else:
                    comment_span = []

                profile_py = ProfileData(
                    name=name,
                    job=job,
                    location=location,
                    skills=[element.get_text().strip() for element in captured_span],
                    experience=[element.get_text().strip() for element in captured_span],
                    certifications=[element.get_text().strip() for element in certification_span],
                    languages=[element.get_text().strip() for element in language_span],
                    recommendations=[element.get_text().strip() for element in recommendation_span],
                    courses=[element.get_text().strip() for element in course_span],
                    organizations=[element.get_text().strip() for element in organisation_span],
                    volunteering=[element.get_text().strip() for element in voluntering_span],
                    activity=[element.get_text().strip() for element in activity_span],
                    comments=[element.get_text() for element in comment_span]
                )

                output_data_py.append(profile_py)
                
                return output_data_py # Return the latest JSON file path
                    
'''
Test to see if script is still working
'''

# # Create an instance of LinkedinScraper
# scraper = LinkedinScraperScript()

# # Set the URLs of LinkedIn profiles you want to scrape
# profile_urls = [
#     "https://www.linkedin.com/in/matt-domi/",

# ]

# # Log in to LinkedIn
# driver = scraper.login_to_linkedin(use_proxy=False)

# scraped_data = scraper.scrape_profiles(driver, profile_urls)
# print(scraped_data)
