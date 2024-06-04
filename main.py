import os
import shutil
from tools_vanilla.link_extractor import extract_linkedin_links_from_pdf
from tools_vanilla.linkedin_scraper import LinkedinScraperScript
from crew import MyCrew


# Define the folders
cv_folder = r'C:\Users\domin\Desktop\sma-crewai-agentmania\CV'
cv_enrichment_in_process_folder = r'C:\Users\domin\Desktop\sma-crewai-agentmania\cv_enrichment_in_process'
cv_enrichment_not_available_folder = r'C:\Users\domin\Desktop\sma-crewai-agentmania\cv_enrichment_not_available'
cv_enrichment_complete_folder = r'C:\Users\domin\Desktop\sma-crewai-agentmania\cv_enrichment_complete'

# Create the folders if they don't exist
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
        shutil.move(cv, cv_enrichment_in_process_folder)
        print(f"CV {cv} has a LinkedIn link and has been moved to {cv_enrichment_in_process_folder}")
        
        # Scrape LinkedIn profiles
        scraped_data = scraper.scrape_profiles(driver, result_single_pdf)
        
        # Access the JSON paths
        path_json_linkedin = scraper.latest_json_path
        
        # Creating a raw string representation
        raw_path_json_linkedin = fr"{path_json_linkedin}"
        
        # Create a unique subfolder for the CV in the cv_enrichment_complete folder
        cv_name = os.path.splitext(os.path.basename(cv))[0]
        cv_subfolder = os.path.join(cv_enrichment_complete_folder, cv_name)
        os.makedirs(cv_subfolder, exist_ok=True)
        
        # Generate a unique JSON filename
        json_filename = f"{cv_name}_cvenrichment.json"
        json_filepath = os.path.join(cv_subfolder, json_filename)
        
        # Run MyCrew with the CV, JSON path, and dynamic output filename
        mycrew = MyCrew(cv, raw_path_json_linkedin, json_filepath)
        result = mycrew.run()
        print(result)
        
        # Move the CV and related JSON to the subfolder
        shutil.move(os.path.join(cv_enrichment_in_process_folder, os.path.basename(cv)), cv_subfolder)
        shutil.move(path_json_linkedin, cv_subfolder)
        print(f"CV {cv} and its related data have been moved to {cv_subfolder}")
    else:
        # Move the CV to the cv_enrichment_not_available folder
        shutil.move(cv, cv_enrichment_not_available_folder)
        print(f"CV {cv} does not have a LinkedIn link and has been moved to {cv_enrichment_not_available_folder}")
