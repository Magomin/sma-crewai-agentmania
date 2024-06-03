from langchain.tools import tool
import os
import fitz
from crewai_tools import BaseTool
from typing import ClassVar




class CvPdfParserTool:

    @staticmethod
    def extract_text_and_links_from_pdf(file_path: str):
        """
        Extract the text and the links stored inside the PDF.

        Parameters:
        - file_path (str): The path to the PDF file.

        Returns:
        - text (str): The extracted text from the PDF.
        - links (list): A list of URLs found in the PDF.
        """
        pdf_document = fitz.open(file_path)
        text = ''
        links = []

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            text += page.get_text()
            page_links = page.get_links()
            for link in page_links:
                if 'uri' in link and link['uri'].startswith(('http://', 'https://')):
                    links.append(link['uri'])

        pdf_document.close()
        return text, links

    def parse_pdf(self, directory_path: str):
        """
        Extract text and links from all PDFs in a specified directory.

        Parameters:
        - directory_path (str): The path to the directory containing PDF files.

        Returns:
        - extracted_data (list): A list of dictionaries with filename, text, and links for each PDF.
        """
        extracted_data = []
        for filename in os.listdir(directory_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                text, links = self.extract_text_and_links_from_pdf(pdf_path)
                extracted_data.append({'filename': filename, 'text': text, 'links': links})
        return extracted_data

    @tool("Search within a PDF using my custom tool")
    def mypdftool(file_path: str):
        """
        Extract text and links from a specified PDF file.

        Parameters:
        - file_path (str): The path to the PDF file.

        Returns:
        - A dictionary containing the filename, text, and links from the specified PDF file.
        """
        file_path = file_path.strip('"')  # Remove extra quotes if present
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        if not file_path.endswith('.pdf'):
            return "Invalid file type. Only PDF files are supported."

        my_pdf_tool = CvPdfParserTool()
        result = my_pdf_tool.parse_pdf(os.path.dirname(file_path))
        for item in result:
            if item['filename'] == os.path.basename(file_path):
                return item
        return "No data extracted from the specified PDF."
    



# class URLTool(BaseTool):
#     name: ClassVar = "URLTool"
#     description: ClassVar = "A tool to format a URL into a specific list format."

#     @tool("A tool to format a URL into a list format.")
#     def url_tool(self, url: str) -> str:
#         """

#         A tool that is useful to format url into a specific list format.

#         """
#         return f"url=['{url}']"





    # @tool("summarization", args_schema=CVProfile, return_direct=True)
    # def summarization(name: str, experience: str, skills: str, education: str, linkedin_url: str) -> CVProfile:
    #     """
    #     Summarize different parts of a CV and return as a Pydantic model.

    #     Parameters:
    #     - name (str): The name of the CV owner (e.g., "name: Olivia Garcia").
    #     - experience (str): The experience of the CV owner (e.g., "experience: Worked for two years at Deloitte as a business developer").
    #     - education (str): The education of the CV owner (e.g., "education: Studied at Oxford for 5 years, got an MBA in business").
    #     - skills (str): The skills of the CV owner (e.g., "skills: good in negotiation, able to work under pressure, know how to code in Python").
    #     - linkedin_url (str): The LinkedIn URL of the CV owner (e.g., "linkedin_url: https://www.linkedin.com/in/example/").

    #     Returns:
    #     - CVProfile: An instance of the CVProfile Pydantic model with the summarized CV details.
    #     """
    #     experience_summary = f"From the CV, it is evident that {experience}"
    #     education_summary = f"The CV indicates that {education}"
    #     skills_summary = f"The CV highlights skills such as {skills}"

    #     summarized_cv = CVProfile(
    #         name=name,
    #         experience=experience_summary,
    #         education=education_summary,
    #         skills=skills_summary,
    #         linkedin_url=linkedin_url
    #     )

    #     return summarized_cv
    




    

    # @tool("Search within PDF content using CrewAI PDFSearchTool")
    # def crewaipdftool(file_path: str, query: str) -> str:
    #     """Use PDFSearchTool for semantic searches within PDF content.
    #     Allows inputting a search query and a PDF document, leveraging advanced search techniques to find relevant content efficiently.
    #     Useful for extracting specific information from large PDF files quickly."""
    #     crewai_pdf_search_tool = PDFSearchTool()
    #     result = crewai_pdf_search_tool.run({'file_path': file_path, 'query': query})
    #     return result
    