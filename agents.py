import os
from textwrap import dedent
from crewai import Agent
from tools_llm.cv_tool import CvPdfParserTool

from crewai_tools import JSONSearchTool
from crewai_tools import FileReadTool
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from anthropic import Anthropic
from langchain_community.chat_models import BedrockChat
from langchain_core.runnables import ConfigurableField
load_dotenv(find_dotenv(), override=True)



chatgpt4= ChatOpenAI(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")
)

_model_kwargs = {
    "temperature": float(os.getenv("BEDROCK_CLAUDE_TEMPERATURE", "0.1")),
    "top_p": float(os.getenv("BEDROCK_CLAUDE_TOP_P", "1")),
    "top_k": int(os.getenv("BEDROCK_CLAUDE_TOP_K", "250")),
    "max_tokens": int(os.getenv("BEDROCK_CLAUDE_MAX_TOKENS_TO_SAMPLE", "300")),
}


claude_3_opus = BedrockChat(
    model_id="anthropic.claude-3-opus-20240307-v1:0",
    region_name="us-east-1",
    model_kwargs=_model_kwargs
)

claude_3_haiku = BedrockChat(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1",
    model_kwargs=_model_kwargs
)


llama_3_8b = ChatOpenAI(
    model="crewai-llama3-8b",
    base_url="http://localhost:11434/v1",
    api_key="NA"
        )
        

filereadtool = FileReadTool()

"""

This is were we create our agents.
an agent is a class that has a name, role, goal, backstory, and tool
you can create your own tool with th @tool decorator, or access the tool created by crewai 
you can also use tool from langchain as crewai is a framework that was build on top of langchain.

im currently using two tools, my own cv tool that you can see find in tools_llm/cv_tool.py
it's purpose is to help the agent that reads the cv to read pdf,

the other tool is FileReadTool, is a tool from crewai, and I've pass it to my summary agent,
so it can read the commented.txt file outputed by the cvcrew, 

"""





class CvCrewAgents:




    def cv_analyzer_agent(self,cv):
        return Agent(
            name="cv information retriever",
            role="retrieve information from a pdf",
            goal=f"""get the information of the {cv}""",
            backstory="""You are a seasoned HR, who is used to analyse CVs"
            to identify key qualifications and skills.""",
            verbose=True,
            memory=True,
            allow_delegation=False,
            tools=[
                CvPdfParserTool.mypdftool,  
            ],
            llm=claude_3_haiku
        )
    
    def cv_verifier_agent(self,cv):
           return Agent(
                name="Cv verifier agent",
                role="verify the commentedcv",
                goal=f"""verify that the information of {cv} was corrreclty extracted""",
                backstory="""You're an amazing reviewer, your used to detect mistakes in your collegues work, 
                correct them to output a better job, and improve the overall quality of the task""",
                tools=[
                       CvPdfParserTool.mypdftool,
                ],
                llm=claude_3_haiku,
                allow_delegation=False
           )
            








class LinkedinCrewAgents:

    def __init__(self):
        self.local_llm = ChatOpenAI(
        model="crewai-llama3-8b",
        base_url="http://localhost:11434/v1",
        api_key="NA"
        )
        


    

    def linkedin_experience_analyzer_agent(self,linkedin_experience):
        
        
        return Agent(
            name="Linkedin information retriever",
            role=f"""Retrieve infomation from {linkedin_experience}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the experience of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )
    def linkedin_skills_analyzer_agent(self,linkedin_skills):
            return Agent(
            name="Linkedin information retriever",
            role=f"""Retrieve infomation from {linkedin_skills}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the skills of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )

    def linkedin_education_analyzer_agent(self,linkedin_education):
            return Agent(
            name="Linkedin information retriever",
            role=f"""Retrieve infomation from {linkedin_education}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the education of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )
    
    def linkedin_languages_analyzer_agent(self,linkedin_languages):
            return Agent(
            name="Linkedin language retriever",
            role=f"""Retrieve infomation from {linkedin_languages}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the languages that are spoken in linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )
    
    def linkedin_recommendations_analyzer_agent(self,linkedin_recommendations):
            return Agent(
            name="Linkedin language agent",
            role=f"""Retrieve infomation from {linkedin_recommendations}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the recommendations of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )
    

    def linkedin_certification_analyzer_agent(self,linkedin_certifications):
            return Agent(
            name="Linkedin certification agent",
            role=f"""Retrieve infomation from {linkedin_certifications}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the certifications of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )

    def linkedin_activity_analyzer_agent(self,linkedin_activity):
            return Agent(
            name="Linkedin activity agent",
            role=f"""Retrieve infomation from {linkedin_activity}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the activity of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )   

    def linkedin_courses_analyzer_agent(self,linkedin_courses):
            return Agent(
            name="Linkedin activity agent",
            role=f"""Retrieve infomation from {linkedin_courses}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the activity of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )   


    def linkedin_organizations_analyzer_agent(self,linkedin_organisations):
            return Agent(
            name="Linkedin activity agent",
            role=f"""Retrieve infomation from {linkedin_organisations}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the activity of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )   

    def linkedin_volunteering_analyzer_agent(self,linkedin_volunteering):
            return Agent(
            name="Linkedin activity agent",
            role=f"""Retrieve infomation from {linkedin_volunteering}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the activity of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku
        )   


    def linkedin_comments_analyzer_agent(self,linkedin_comments):
            return Agent(
            name="Linkedin activity agent",
            role=f"""Retrieve infomation from {linkedin_comments}
                                """,
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a pydantic, and analyse it as professional HR Agent",
            backstory="""You're a seasoned human ressource proffesional, you have lot of
            expertise analysing  the activity of linkedin profiles and getting information out of them especially if
            they are stored as pydantic object """,
            verbose=True,
            memory=True,
            tool=[
                
          
            ],
            allow_delegation=False,
            llm=claude_3_haiku,
        )   



    def sumarizer_agent(self):
        return Agent(
            name="summarizer",
            role="Summarize the main information of the LinkedIn profile and enrich the cv with that info",
            goal="Your goal is to summarize the main information of the LinkedIn profile",
            backstory="You have extensive experience in summarizing LinkedIn profiles, and comparing that with the info present in their cv to enrich it",
            llm=claude_3_haiku,
            allow_delegation=False
        )
    


    def  enrichment_verifier_agent(self):
           return Agent(
                  name="Enrichement Verifier",
                  role="Verify the cvenrichement",
                  goal=f"""your goal is to verify that the cv enrichement was correclty done, the information correspond to the cv, and the linkedin profile aswell""",
                  backstory="You're an amazing reviewer, your used to detect mistakes in your collegues work, correct them to output a better job, and improve the overall quality of the task",
                  llm=claude_3_haiku,
                  allow_delegation=False
           ) 





