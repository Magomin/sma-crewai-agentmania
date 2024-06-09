import os
import shutil
import json
from tools_vanilla.link_extractor import extract_linkedin_links_from_pdf
from tools_vanilla.linkedin_scraper import LinkedinScraperScript
from multiplecrew import CvCrew, LinkedinCrew
from concurrent.futures import ThreadPoolExecutor, as_completed



"""

Hello to you!
This is the main script for the Cv enrichement .



    Here we define the flow of the script, we run the cvcrew and linkedincrew
    as well as the linkedin scraper, in order to enrich the cv

    -first we run a tool to detects the linkedin links in the cv, 
    if there is a linkedin link we move the cv to the cv_enrichment_in_process folder
    and we run the cvcrew

    -if there is no linkedin link we move the cv to the cv_enrichment_not_available folder

    -the cvcrew will return a commented cv file which the linkedin crew will use

    -the linkedin scraper scrap the linkedin profile of the linkedin link in paralel
    to the cvcrew once finish, the linkedin crew will start as it has all the info it needs

    -the linkedin crew will return a enriched cv file and place both the cv and the enriched cv in the cv_enrichment_complete folder


HOW TO USE:

        1.Be sure that there is a working account in the LinkedinScraperScript

        2.Place the CVs in the CV folder and run the script

        3.Run main.py 


"""





# Load configuration
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

# Get the base directory (the directory where the script is located)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define folders based on configuration
cv_folder = os.path.join(base_dir, config['cv_folder'])
cv_enrichment_in_process_folder = os.path.join(base_dir, config['cv_enrichment_in_process_folder'])
cv_enrichment_not_available_folder = os.path.join(base_dir, config['cv_enrichment_not_available_folder'])
cv_enrichment_complete_folder = os.path.join(base_dir, config['cv_enrichment_complete_folder'])
output_directory = os.path.join(base_dir, config['output_directory'])

# Path to commented_cv.txt and cv_enrichment.txt
commented_cv_path = os.path.join(output_directory, 'commented_cv.txt')
cv_enrichment_path = os.path.join(output_directory, 'cv_enrichment.txt')

# Create folders if they don't exist
os.makedirs(cv_enrichment_in_process_folder, exist_ok=True)
os.makedirs(cv_enrichment_not_available_folder, exist_ok=True)
os.makedirs(cv_enrichment_complete_folder, exist_ok=True)

# Initialize scraper and login
scraper = LinkedinScraperScript()
driver = scraper.login_to_linkedin(use_proxy=False)

# Fetch all CVs from the specified directory
cvs = [os.path.join(cv_folder, f) for f in os.listdir(cv_folder) if f.lower().endswith('.pdf')]

# Function to run CvCrew
def run_cv_crew(cv_path):
    cv_crew = CvCrew(cv_path)
    cv_crew.run()

# Function to scrape LinkedIn profiles
def scrape_linkedin_profiles(linkedin_links):
    return scraper.scrape_profiles(driver, linkedin_links)

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

        with ThreadPoolExecutor() as executor:
            # Submit the CvCrew and LinkedIn scraping tasks to the executor
            futures = {
                executor.submit(run_cv_crew, cv_in_process_path): 'cv_crew',
                executor.submit(scrape_linkedin_profiles, result_single_pdf): 'linkedin_scrape'
            }

            linkedin_data = None
            for future in as_completed(futures):
                task = futures[future]
                if task == 'linkedin_scrape':
                    linkedin_data = future.result()
                elif task == 'cv_crew':
                    future.result()

        # Extract data from LinkedIn scraping results
        (name, linkedin_experience, linkedin_skills, linkedin_education,
         linkedin_certifications, linkedin_languages, linkedin_recommendations,
         linkedin_courses, linkedin_organizations, linkedin_volunteering, 
         linkedin_activity, linkedin_comments) = linkedin_data
        
        print(linkedin_data)

        # Assuming LinkedinCrew can now accept the profiles directly
        linkedin_crew = LinkedinCrew(name, linkedin_experience, linkedin_skills, linkedin_education, 
                                     linkedin_certifications, linkedin_languages, linkedin_recommendations,
                                     linkedin_courses, linkedin_organizations, linkedin_volunteering, 
                                     linkedin_activity, linkedin_comments, commented_cv_path)
        linkedin_crew.run()
        
       
    
            
        # Create subfolder in cv_enrichment_complete_folder for the CV
        cv_base_name = os.path.splitext(os.path.basename(cv_in_process_path))[0]
        cv_subfolder = os.path.join(cv_enrichment_complete_folder, cv_base_name)
        os.makedirs(cv_subfolder, exist_ok=True)

        # Move cv_enrichment.txt to the subfolder if it exists
        if os.path.exists(cv_enrichment_path):
            cv_enrichment_complete_path = os.path.join(cv_subfolder, 'cv_enrichment.txt')
            shutil.move(cv_enrichment_path, cv_enrichment_complete_path)
            print(f"cv_enrichment.txt has been moved to {cv_subfolder}")
        else:
            print(f"cv_enrichment.txt does not exist when trying to move it to {cv_subfolder}")

        # Move the CV to the subfolder
        cv_complete_path = os.path.join(cv_subfolder, os.path.basename(cv_in_process_path))
        shutil.move(cv_in_process_path, cv_complete_path)
        print(f"CV {cv_in_process_path} has been moved to {cv_subfolder}")

        # Clean up
        if os.path.exists(commented_cv_path):
            os.remove(commented_cv_path)
            print(f"commented_cv.txt has been deleted.")