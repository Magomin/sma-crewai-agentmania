import os
import shutil
import json
from tools_vanilla.link_extractor import extract_linkedin_links_from_pdf
from tools_vanilla.linkedin_scraper import LinkedinScraperScript
from crew import MyCrew

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

        # Scrape LinkedIn profiles
        path_json_linkedin = scraper.scrape_profiles(driver, result_single_pdf)
        
        # Debug: Check if the JSON file exists
        if not os.path.exists(path_json_linkedin):
            print(f"Error: The JSON file {path_json_linkedin} does not exist.")
            continue
        
        print(f"Scraped data saved to: {path_json_linkedin}")

        # Create a unique subfolder for the CV in the cv_enrichment_complete folder
        cv_name = os.path.splitext(os.path.basename(cv))[0]
        cv_subfolder = os.path.join(cv_enrichment_complete_folder, cv_name)
        os.makedirs(cv_subfolder, exist_ok=True)
        
        # Move the CV to the subfolder
        cv_final_path = os.path.join(cv_subfolder, os.path.basename(cv_in_process_path))
        shutil.move(cv_in_process_path, cv_final_path)
        print(f"CV moved to: {cv_final_path}")

        # Debug: Print path before running MyCrew
        print(f"Running MyCrew with CV path: {cv_final_path} and LinkedIn JSON path: {path_json_linkedin}")
        
        # Run MyCrew and save the result to another JSON file in the subfolder
        mycrew = MyCrew(cv_final_path, path_json_linkedin)
        
        # Debug: Check if MyCrew can access the JSON file
        try:
            mycrew_result = mycrew.run()
        except Exception as e:
            print(f"Error running MyCrew: {e}")
            continue
        
        mycrew_json_filename = f"{cv_name}_mycrew_data.json"
        with open(os.path.join(cv_subfolder, mycrew_json_filename), 'w') as f:
            json.dump(mycrew_result, f)
        print(f"CV {cv} and its related data have been moved to {cv_subfolder}")
    else:
        # Move the CV to the cv_enrichment_not_available folder
        shutil.move(cv, cv_enrichment_not_available_folder)
        print(f"CV {cv} does not have a LinkedIn link and has been moved to {cv_enrichment_not_available_folder}")