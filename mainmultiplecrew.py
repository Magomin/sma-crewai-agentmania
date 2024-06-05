import os
import shutil
import json
from tools_vanilla.link_extractor import extract_linkedin_links_from_pdf
from tools_vanilla.linkedin_scraper import LinkedinScraperScript
from multiplecrew import CvCrew,LinkedinCrew

# Define folders
cv_folder = r'C:\Users\domin\Desktop\sma-crewai-agentmania\CV'
cv_enrichment_in_process_folder = r'C:\Users\domin\Desktop\sma-crewai-agentmania\cv_enrichment_in_process'
cv_enrichment_not_available_folder = r'C:\Users\domin\Desktop\sma-crewai-agentmania\cv_enrichment_not_available'
cv_enrichment_complete_folder = r'C:\Users\domin\Desktop\sma-crewai-agentmania\cv_enrichment_complete'

# Create folders if they don't exist
os.makedirs(cv_enrichment_in_process_folder, exist_ok=True)
os.makedirs(cv_enrichment_not_available_folder, exist_ok=True)
os.makedirs(cv_enrichment_complete_folder, exist_ok=True)

# Initialize scraper and login
scraper = LinkedinScraperScript()
driver = scraper.login_to_linkedin(use_proxy=False)

# Fetch all CVs from the specified directory
cvs = [os.path.join(cv_folder, f) for f in os.listdir(cv_folder) if f.lower().endswith('.pdf')]

# Loop through the CVs
for cv in cvs:
    # Extract LinkedIn links from the CV
    result_single_pdf = extract_linkedin_links_from_pdf(cv)
    
    # Check if there is at least one LinkedIn link
    if result_single_pdf:
        # Move the CV to the cv_enrichment_in_process folder temporarily
        cv_in_process_path = os.path.join(cv_enrichment_in_process_folder, os.path.basename(cv))
        shutil.move(cv, cv_in_process_path)
        print(f"CV {cv} has a LinkedIn link and has been moved to {cv_enrichment_in_process_folder}")
        
        cv_crew=CvCrew(cv_in_process_path)
        cv_crew.run()


        # Scrape LinkedIn profiles
        scraped_profiles = scraper.scrape_profiles(driver, result_single_pdf)

        # You can now access the scraped_profiles directly
        print(scraped_profiles)

        # If LinkedinCrew requires a path, you'll need to modify it to accept the profiles directly or save them to JSON if absolutely necessary
        # Here, assuming LinkedinCrew can now accept the profiles directly
        linkedin_crew = LinkedinCrew(scraped_profiles)
        linkedin_crew.run()
