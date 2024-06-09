import os
import fitz



"""
Tools_vanilla folder contains script that i find better to use without LLMs, as they are prone to error, 
and the tools work well on their own

link_extractor is to verify and extract the linkedin link on the cv, 
linkedin_scraper is to extract data from the linkedin profiles

"""

def extract_linkedin_links_from_pdf(file_path: str):
    """
    Extract the LinkedIn URLs stored inside the PDF.

    Parameters:
    - file_path (str): The path to the PDF file.

    Returns:
    - linkedin_links (list): A list of LinkedIn URLs found in the PDF.
    """
    pdf_document = fitz.open(file_path)
    linkedin_links = []

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        page_links = page.get_links()
        for link in page_links:
            if 'uri' in link and link['uri'].startswith(('http://', 'https://')):
                url = link['uri']
                if 'linkedin.com' in url:
                    linkedin_links.append(url)

    pdf_document.close()
    return linkedin_links

def extract_linkedin_links_from_directory(directory_path: str):
    """
    Extract LinkedIn links from all PDFs in a specified directory.

    Parameters:
    - directory_path (str): The path to the directory containing PDF files.

    Returns:
    - extracted_data (list): A list of dictionaries with filename and LinkedIn links for each PDF.
    """
    extracted_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            linkedin_links = extract_linkedin_links_from_pdf(pdf_path)
            extracted_data.append({'filename': filename, 'linkedin_links': linkedin_links})
    return extracted_data


