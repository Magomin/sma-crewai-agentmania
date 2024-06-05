import os
from crewai import Crew,Process
from textwrap import dedent
from langchain_anthropic import ChatAnthropic
from agents import InformationAnalystAgents,InformationRetrieverAgents
from tasks import CvTasks,LinkedinTasks,EnrichementTasks,ComparaisonTasks
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import BedrockChat
from langchain_core.runnables import ConfigurableField

load_dotenv(find_dotenv(), override=True)

_model_kwargs = {
    "temperature": float(os.getenv("BEDROCK_CLAUDE_TEMPERATURE", "0.1")),
    "top_p": float(os.getenv("BEDROCK_CLAUDE_TOP_P", "1")),
    "top_k": int(os.getenv("BEDROCK_CLAUDE_TOP_K", "250")),
    "max_tokens": int(os.getenv("BEDROCK_CLAUDE_MAX_TOKENS_TO_SAMPLE", "300")),
}


#Models

chatgpt4= ChatOpenAI(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")
)

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
        

class CvCrew:
    def __init__(self,cv):
        self.cv =cv

    def run(self):

        agents = (InformationRetrieverAgents(),InformationAnalystAgents())
        tasks = (CvTasks())



        """
        
        Agents
        """
        #information retriever agents
        cv_info_retriever_agent = agents[0].cv_info_retriever_agent(self.cv)
        cv_information_analyst_agent=agents[1].cv_information_analyst_agent()

        """
        Tasks
        """

        #CV Tasks
        get_cvprofile_task=tasks.get_cvprofile_task(cv_info_retriever_agent,self.cv)
        comment_cv_task=tasks.comment_cv_task(cv_information_analyst_agent,[get_cvprofile_task])

        #CvCrew
        cv_crew = Crew(
            agents=[

               cv_info_retriever_agent,
               cv_information_analyst_agent,
         
            ],
            tasks=[

                get_cvprofile_task,
                comment_cv_task,

            ],
            verbose=True,
            process=Process.sequential,
            manager_llm= claude_3_haiku,
        )

        result_cv_crew = cv_crew.kickoff()
        return result_cv_crew

class LinkedinCrew:
    def __init__(self,linkdedinpydantic):
        self.linkedinpydantic = linkdedinpydantic
        
    def run(self):

        

        agents = (InformationRetrieverAgents(),InformationAnalystAgents())
        tasks =  (LinkedinTasks())

        """
        Agents
        """
        #information retriever agents
        linkedin_info_retriever_agent=agents[0].linkedin_info_retriever_agent(self.linkedinpydantic)

        #Information analyst agents
        linkedin_information_analyst_agent=agents[1].linkedin_information_analyst_agent()

       

        """
        Tasks
        """


        #Linkedin Tasks
        get_linkedin_profile_task=tasks.get_linkedin_profile_task(linkedin_info_retriever_agent,self.linkedinpydantic)
        comment_linkedin_profile_task=tasks.comment_linkedin_profile_task(linkedin_information_analyst_agent,[get_linkedin_profile_task])

        


        




        #Define your custom Crew here
        linkedin_crew = Crew(
            agents=[


               linkedin_info_retriever_agent,
               linkedin_information_analyst_agent,

                
            ],
            tasks=[
                get_linkedin_profile_task,
                comment_linkedin_profile_task,
         
            ],
            verbose=True,
            process=Process.sequential,
            manager_llm= claude_3_haiku
        )

        result = linkedin_crew.kickoff()
        return result
    