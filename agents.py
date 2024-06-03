import os
from textwrap import dedent
from crewai import Agent
from crewai_tools import JSONSearchTool
from tools_llm.cv_tool import CvPdfParserTool
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
        

json_search_tool = JSONSearchTool()

class InformationRetrieverAgents:
    def __init__(self):
        self.local_llm = ChatOpenAI(
        model="crewai-llama3-8b",
        base_url="http://localhost:11434/v1",
        api_key="NA"
        )
        
        
    def cv_info_retriever_agent(self,cv):
        return Agent(
            name="cv information retriever",
            role="retrieve information from a pdf",
            goal=f"""get the most important information of the {cv}""",
            backstory="""Your the most experienced pdf analyst, you have lot of
            expertise analysing cv and getting information out of them especially if
            they are stored as pdf format """,
            verbose=True,
            memory=True,
            allow_delegation=False,
            tools=[
                CvPdfParserTool.mypdftool,  
            ],
            max_iter=15,
            llm=chatgpt4
        )
    

    def linkedin_info_retriever_agent(self,json):

        return Agent(
            name="Linkedin information retriever",
            role=f"Retrieve infomation from {json}",
            goal="Your goal is to retrieve important information of a linkedin profile that is stored as a json",
            backstory="""Your the most experienced json analyst, you have lot of
            expertise analysing linkedin profile and getting information out of them especially if
            they are stored as json format """,
            verbose=True,
            memory=True,
            tool=[
                json_search_tool    
            ],
            allow_delegation=False,
            llm=chatgpt4
        )

class InformationAnalystAgents:
    
    def cv_information_analyst_agent(self):
        return Agent(
            name="CV Information Analyst Agent", 
            role="Analyze the information of the CV",
            goal="Your goal is to provide an analysis of the information of the CV",
            backstory="You have extensive experience in reviewing and analyzing CVs"
            "to identify key qualifications and skills.",
            verbose=True,
            memory=True,
            allow_delegation=False,
            llm=chatgpt4
        )

    def linkedin_information_analyst_agent(self):
        return Agent(
            name="LinkedIn Information Analyst Agent",
            role="Analyze the information of the LinkedIn profile",
            goal="Your goal is to extract and analyze information from the LinkedIn profile",
            backstory="You have a strong background in social media analysis, particularly focusing on professional profiles like LinkedIn.",
            verbose=True,
            memory=True,
            allow_delegation=False,
            llm=chatgpt4
        )

    def information_comparaison_agent(self):
        return Agent(
            name="Information Comparison Agent",
            role="Compare the information from the CV and LinkedIn profiles",
            goal="Your goal is to provide a detailed comparison of the information found in the CV and LinkedIn profiles",
            backstory="You specialize in comparing and contrasting data from different sources to provide comprehensive insights.",
            verbose=True,
            memory=True,
            allow_delegation=False,
            llm=chatgpt4
        )

    def enrichement_agent(self):
        return Agent(
            name="Enrichment Agent",
            role="Enrich the CV",
            goal="Your goal is to provide a paragraph that enriches the CV using information from the LinkedIn profile",
            backstory="""You are a seasoned Human Resources agent with extensive experience in identifying key information that helps candidates stand out.""",
            verbose=True,
            memory=True,
            allow_delegation=False,
            llm=chatgpt4
        )
