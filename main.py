from tools_vanilla.link_extractor import extract_linkedin_links_from_pdf
from tools_vanilla.linkedin_scraper import LinkedinScraperScript
from crew import MyCrew

# Initialize scraper and login
scraper = LinkedinScraperScript()
driver = scraper.login_to_linkedin(use_proxy=False)

# Extract LinkedIn links from PDF
cv = r"C:\Users\domin\Desktop\sma-crewai-agentmania\CV\Cv Matthieu Dominguez Business developer.pdf"
result_single_pdf = extract_linkedin_links_from_pdf(cv)



# Scrape LinkedIn profiles and save data
scraped_data = scraper.scrape_profiles(driver, result_single_pdf)

# Access the JSON paths
path_json_linkedin=scraper.latest_json_path

# Creating a raw string representation
raw_path_json_linkedin = fr"{path_json_linkedin}"



mycrew = MyCrew(cv,json=raw_path_json_linkedin)
result = mycrew.run()
print(result)

